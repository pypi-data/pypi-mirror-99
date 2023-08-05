""".. Ignore pydocstyle D400.

=================
Collection Tables
=================

.. autoclass:: CollectionTables
    :members:

    .. automethod:: __init__
"""
import os
from functools import lru_cache
from io import BytesIO
from typing import Dict, List, Optional
from urllib.parse import urljoin

import pandas as pd
import pytz
from tqdm import tqdm

from resdk.resources.utils import iterate_schema

from .resolwe import Resolwe
from .resources import Collection, Data, Sample
from .utils.table_cache import (
    cache_dir_resdk,
    clear_cache_dir_resdk,
    load_pickle,
    save_pickle,
)

EXP = "exp"
RC = "rc"
META = "meta"

SAMPLE_FIELDS = ["id", "slug", "name", "descriptor", "descriptor_schema"]
DATA_FIELDS = [
    "id",
    "slug",
    "modified",
    "entity__name",
    "output",
    "process__output_schema",
]

CHUNK_SIZE = 1000


class CollectionTables:
    """A helper class to fetch collection's expression and meta data.

    This class enables fetching given collection's data and returning it as tables
    which have samples in rows and expressions/metadata in columns.

    When calling :attr:`CollectionTables.exp`, :attr:`CollectionTables.rc` and
    :attr:`CollectionTables.meta` for the first time the corresponding data gets
    downloaded from the server. This data than gets cached in memory and on disc and is
    used in consequent calls. If the data on the server changes the updated version
    gets re-downloaded.

    A simple example:

    .. code-block:: python

        # get Collection object
        collection = res.collection.get("collection_slug")

        # fetch collection expressions and metadata
        tables = CollectionTables(collection)
        exp = tables.exp
        rc = tables.rc
        meta = tables.meta

    """

    def __init__(self, collection: Collection, cache_dir: Optional[str] = None):
        """Initialize class.

        :param collection: collection to use
        :param cache_dir: cache directory location, if not specified system specific
                          cache directory is used
        """
        self.resolwe = collection.resolwe  # type: Resolwe
        self.collection = collection

        self.cache_dir = cache_dir
        if self.cache_dir is None:
            self.cache_dir = cache_dir_resdk()
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.gene_ids = []  # type: List[str]

    @property
    @lru_cache()
    def meta(self) -> pd.DataFrame:
        """Return samples metadata table as a pandas DataFrame object.

        :return: table of metadata
        """
        return self._load_fetch(META)

    @property
    @lru_cache()
    def exp(self) -> pd.DataFrame:
        """Return expressions table as a pandas DataFrame object.

        Which type of expressions (TPM, CPM, FPKM, ...) get returned depends on how the
        data was processed. The expression type can be checked in the returned table
        attribute `attrs['exp_type']`:

        .. code-block:: python

            exp = tables.exp
            print(exp.attrs['exp_type'])

        :return: table of expressions
        """
        exp = self._load_fetch(EXP)
        self.gene_ids = exp.columns.tolist()
        return exp

    @property
    @lru_cache()
    def rc(self) -> pd.DataFrame:
        """Return expression counts table as a pandas DataFrame object.

        :return: table of counts
        """
        rc = self._load_fetch(RC)
        self.gene_ids = rc.columns.tolist()
        return rc

    @property
    @lru_cache()
    def id_to_symbol(self) -> Dict[str, str]:
        """Map of source gene ids to symbols.

        This also gets fetched only once and then cached in memory and on disc.
        :attr:`CollectionTables.exp` or :attr:`CollectionTables.rc` must be called
        before this as the mapping is specific to just this data. Its intended use is
        to rename table column labels from gene ids to symbols.

        Example of use:

        .. code-block:: python

            exp = exp.rename(columns=tables.id_to_symbol)

        :return: dict with gene ids as keys and gene symbols as values
        """
        species = self._data[0].output["species"]
        source = self._data[0].output["source"]

        if not self.gene_ids:
            raise ValueError("Expression data must be used before!")

        return self._mapping(self.gene_ids, source, species)

    @staticmethod
    def clear_cache() -> None:
        """Remove ReSDK cache files from the default cache directory."""
        clear_cache_dir_resdk()

    @property
    @lru_cache()
    def _samples(self) -> List[Sample]:
        """Fetch sample objects.

        Fetch all samples from given collection and cache the results in memory. Only
        the needed subset of fields is fetched.

        :return: list od Sample objects
        """
        return list(self.collection.samples.filter(fields=SAMPLE_FIELDS))

    @property
    @lru_cache()
    def _data(self) -> List[Data]:
        """Fetch data objects.

        Fetch expression data objects from given collection and cache the results in
        memory. Only the needed subset of fields is fetched.

        :return: list of Data objects
        """
        return list(
            self.collection.data.filter(type="data:expression:", fields=DATA_FIELDS)
        )

    @property
    @lru_cache()
    def _metadata_version(self) -> str:
        """Return server metadata version.

        The versioning of metadata on the server is determined by the
        newest of these values:

            - newset modified sample
            - newset modified relation
            - newset modified orange Data

        :return: metadata version
        """
        timestamps = []
        kwargs = {
            "ordering": "-modified",
            "fields": ["id", "modified"],
            "limit": 1,
        }

        try:
            newest_sample = self.collection.samples.get(**kwargs)
            timestamps.append(newest_sample.modified)
        except LookupError:
            raise ValueError(
                f"Collection {self.collection.name} has no samples!"
            ) from None

        try:
            newest_relation = self.collection.relations.get(**kwargs)
            timestamps.append(newest_relation.modified)
        except LookupError:
            pass

        try:
            orange = self._get_orange_object()
            timestamps.append(orange.modified)
        except LookupError:
            pass

        newest_modified = sorted(timestamps)[-1]
        # transform into UTC so changing timezones won't effect cache
        version = (
            newest_modified.astimezone(pytz.utc).isoformat().replace("+00:00", "Z")
        )
        return version

    @property
    @lru_cache()
    def _expression_version(self) -> str:
        """Return server expression data version.

        The versioning of expression data on the server is determined by the hash of
        the tuple of sorted data objects ids.

        :return: expression data version
        """
        data_ids = self.collection.data.filter(type="data:expression:", fields=["id"])
        if len(data_ids) == 0:
            raise ValueError(
                f"Collection {self.collection.name} has no expression data!"
            )
        data_ids = tuple(sorted(d.id for d in data_ids))
        version = str(hash(data_ids))
        return version

    def _load_fetch(self, data_type: str) -> pd.DataFrame:
        """Load data from disc or fetch it from server and cache it on disc."""
        data = load_pickle(self._cache_file(data_type))
        if data is None:
            if data_type == META:
                data = self._download_metadata()
            else:
                data = self._download_expressions(data_type)
            save_pickle(data, self._cache_file(data_type))
        return data

    def _cache_file(self, data_type: str) -> str:
        """Return full cache file path."""
        version = (
            self._metadata_version if data_type == META else self._expression_version
        )
        cache_file = f"{self.collection.slug}_{data_type}_{version}.pickle"
        return os.path.join(self.cache_dir, cache_file)

    def _get_descriptors(self) -> pd.DataFrame:
        descriptors = []
        for sample in self._samples:
            sample.descriptor["sample_name"] = sample.name
            descriptors.append(sample.descriptor)

        df = pd.json_normalize(descriptors).set_index("sample_name")

        # Keep only numeric / string types:
        column_types = {}
        prefix = "XXX"
        for (schema, _, path) in iterate_schema(
            sample.descriptor, sample.descriptor_schema.schema, path=prefix
        ):
            field_type = schema["type"]
            field_name = path[len(prefix) + 1 :]

            # This can happen if this filed has None value in all descriptors
            if field_name not in df:
                continue

            if field_type == "basic:string:":
                column_types[field_name] = str
            elif field_type == "basic:integer:":
                # Pandas cannot cast NaN's to int, but it can cast them
                # to pd.Int64Dtype
                column_types[field_name] = pd.Int64Dtype()
            elif field_type == "basic:decimal:":
                column_types[field_name] = float

        df = df[column_types.keys()].astype(column_types)

        return df

    def _get_relations(self) -> pd.DataFrame:
        relations = pd.DataFrame(index=[s.name for s in self._samples])
        relations.index.name = "sample_name"

        id_to_name = {s.id: s.name for s in self._samples}

        for relation in self.collection.relations:
            relations[relation.category] = pd.Series(
                index=relations.index, dtype="object"
            )

            for partition in relation.partitions:
                value = ""
                if partition["label"] and partition["position"]:
                    value = f'{partition["label"]} / {partition["position"]}'
                elif partition["label"]:
                    value = partition["label"]
                elif partition["position"]:
                    value = partition["position"]

                sample_name = id_to_name[partition["entity"]]
                relations[relation.category][sample_name] = value

        return relations

    @lru_cache()
    def _get_orange_object(self) -> Data:
        return self.collection.data.get(
            process__slug="upload-orange-metadata",
            ordering="-modified",
            fields=DATA_FIELDS,
            limit=1,
        )

    def _get_orange_data(self) -> pd.DataFrame:
        try:
            orange_meta = self._get_orange_object()
        except LookupError:
            return pd.DataFrame()

        file_name = orange_meta.files(field_name="table")[0]
        url = urljoin(self.resolwe.url, f"data/{orange_meta.id}/{file_name}")
        response = self.resolwe.session.get(url, auth=self.resolwe.auth)
        response.raise_for_status()

        with BytesIO() as f:
            f.write(response.content)
            f.seek(0)
            if file_name.endswith("xls"):
                df = pd.read_excel(f, engine="xlrd")
            elif file_name.endswith("xlsx"):
                df = pd.read_excel(f, engine="openpyxl")
            elif any(file_name.endswith(ext) for ext in ["tab", "tsv"]):
                df = pd.read_csv(f, sep="\t")
            elif file_name.endswith("csv"):
                df = pd.read_csv(f)
            else:
                # TODO: logging, warning?
                return pd.DataFrame()

        if "mS#Sample ID" in df.columns:
            mapping = {s.id: s.name for s in self._samples}
            df["sample_name"] = [mapping[value] for value in df["mS#Sample ID"]]
            df = df.drop(columns=["mS#Sample ID"])
        elif "mS#Sample slug" in df.columns:
            mapping = {s.slug: s.name for s in self._samples}
            df["sample_name"] = [mapping[value] for value in df["mS#Sample slug"]]
            df = df.drop(columns=["mS#Sample slug"])
        elif "mS#Sample name" in df.columns:
            df = df.rename(columns={"mS#Sample name": "sample_name"})

        return df.set_index("sample_name")

    def _download_metadata(self) -> pd.DataFrame:
        """Download samples metadata and transform into table."""
        meta = pd.DataFrame(None, index=[s.name for s in self._samples])

        # Add descriptors metadata
        descriptors = self._get_descriptors()
        meta = meta.merge(descriptors, how="right", left_index=True, right_index=True)

        # Add relations metadata
        relations = self._get_relations()
        how = "outer" if len(meta.columns) else "right"
        meta = meta.merge(relations, how=how, left_index=True, right_index=True)

        # Add Orange clinical metadata
        orange_data = self._get_orange_data()
        if not orange_data.empty:
            how = "right" if meta.columns.empty else "outer"
            meta = meta.merge(orange_data, how=how, left_index=True, right_index=True)

        meta.index.name = "sample_name"

        return meta

    def _expression_file_url(self, data: Data, exp_type: str) -> str:
        exp_files = data.files(field_name=exp_type)

        if not exp_files:
            raise LookupError(
                f"Data {data.slug} has no expressions of type {exp_type}!"
            )
        elif len(exp_files) > 1:
            raise LookupError(
                f"Data {data.slug} has multiple expressions of type {exp_type}!"
            )

        return urljoin(self.resolwe.url, f"data/{data.id}/{exp_files[0]}")

    def _download_expressions(self, exp_type: str) -> pd.DataFrame:
        """Download expression files and marge them into a pandas DataFrame.

        :param exp_type: expression type
        :return: table with expression data, genes in columns, samples in rows
        """
        df_list = []
        for data in tqdm(self._data, desc="Downloading expressions", ncols=100):
            response = self.resolwe.session.get(
                self._expression_file_url(data, exp_type), auth=self.resolwe.auth
            )
            response.raise_for_status()
            with BytesIO() as f:
                f.write(response.content)
                f.seek(0)
                df_ = pd.read_csv(f, sep="\t", compression="gzip")
                df_ = df_.set_index("Gene").T
                df_.index = [data._original_values["entity"]["name"]]
                df_list.append(df_)

        df = pd.concat(df_list, axis=0).sort_index().sort_index(axis=1)
        source = self._data[0].output["source"]
        df.columns.name = source.capitalize() if source == "ENSEMBL" else source
        df.index.name = "sample_name"
        df.attrs["exp_type"] = (
            "rc" if exp_type == RC else self._data[0].output["exp_type"]
        )
        return df

    def _mapping(self, ids: List[str], source: str, species: str) -> Dict[str, str]:
        """Fetch and cache gene mapping."""
        mapping_cache = os.path.join(self.cache_dir, f"{source}_{species}.pickle")
        mapping = load_pickle(mapping_cache)
        if mapping is None:
            mapping = {}

        # download only the genes that are not in cache
        diff = list(set(ids) - set(mapping.keys()))
        if diff:
            diff_mapping = self._download_mapping(diff, source, species)
            mapping.update(diff_mapping)
            save_pickle(mapping, mapping_cache, override=True)
        return mapping

    def _download_mapping(
        self, ids: List[str], source: str, species: str
    ) -> Dict[str, str]:
        """Download gene mapping."""
        sublists = [ids[i : i + CHUNK_SIZE] for i in range(0, len(ids), CHUNK_SIZE)]
        mapping = {}
        for sublist in tqdm(sublists, desc="Downloading gene mapping", ncols=100):
            features = self.resolwe.feature.filter(
                source=source, species=species, feature_id__in=sublist
            )
            mapping.update({f.feature_id: f.name for f in features})
        return mapping
