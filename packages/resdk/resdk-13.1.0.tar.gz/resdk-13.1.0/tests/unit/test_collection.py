"""
Unit tests for resdk/resources/collection.py file.
"""


import unittest

from mock import MagicMock, patch

from resdk.resources.collection import BaseCollection, Collection
from resdk.resources.data import Data
from resdk.resources.descriptor import DescriptorSchema
from resdk.resources.process import Process

DATA0 = MagicMock(**{"files.return_value": [], "id": 0})

DATA1 = MagicMock(**{"files.return_value": ["reads.fq", "arch.gz"], "id": 1})

DATA2 = MagicMock(**{"files.return_value": ["outfile.exp"], "id": 2})


class TestBaseCollection(unittest.TestCase):
    def test_data_types(self):
        resolwe = MagicMock()

        data1 = Data(resolwe=resolwe, id=1)
        data1._process = Process(resolwe=resolwe, type="data:reads:fastq:single:")

        collection = Collection(resolwe=resolwe, id=1)
        collection._data = [data1]

        types = collection.data_types()
        self.assertEqual(types, ["data:reads:fastq:single:"])

    def test_files(self):
        collection = Collection(resolwe=MagicMock(), id=1)
        collection._data = [DATA1, DATA2]

        files = collection.files()
        self.assertCountEqual(files, ["arch.gz", "reads.fq", "outfile.exp"])


class TestBaseCollectionDownload(unittest.TestCase):
    @patch("resdk.resources.collection.BaseCollection", spec=True)
    def test_field_name(self, collection_mock):
        collection_mock.configure_mock(data=[DATA0, DATA2], resolwe=MagicMock())
        BaseCollection.download(collection_mock, field_name="output.exp")
        flist = ["2/outfile.exp"]
        collection_mock.resolwe._download_files.assert_called_once_with(flist, None)

        # Check if ``output_field`` does not start with 'output'
        collection_mock.reset_mock()
        collection_mock.configure_mock(data=[DATA1, DATA0], resolwe=MagicMock())
        BaseCollection.download(collection_mock, field_name="fastq")
        flist = ["1/reads.fq", "1/arch.gz"]
        collection_mock.resolwe._download_files.assert_called_once_with(flist, None)

    def test_bad_field_name(self):
        collection = Collection(resolwe=MagicMock(), id=1)
        with self.assertRaisesRegex(ValueError, "Invalid argument value `field_name`."):
            collection.download(field_name=123)


class TestCollection(unittest.TestCase):
    def test_descriptor_schema(self):
        collection = Collection(id=1, resolwe=MagicMock())
        collection._descriptor_schema = 1

        # test getting descriptor schema attribute
        self.assertEqual(collection.descriptor_schema, 1)

        # descriptor schema is not set
        collection._descriptor_schema = None
        self.assertEqual(collection.descriptor_schema, None)

        # hidrated descriptor schema
        descriptor_schema = {
            "slug": "test-schema",
            "name": "Test schema",
            "version": "1.0.0",
            "schema": [
                {
                    "default": "56G",
                    "type": "basic:string:",
                    "name": "description",
                    "label": "Object description",
                }
            ],
            "id": 1,
        }
        collection = Collection(
            id=1, descriptor_schema=descriptor_schema, resolwe=MagicMock()
        )
        self.assertTrue(isinstance(collection.descriptor_schema, DescriptorSchema))

        self.assertEqual(collection.descriptor_schema.slug, "test-schema")

    def test_data(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting data attribute
        collection.resolwe.data.filter = MagicMock(
            return_value=["data_1", "data_2", "data_3"]
        )
        self.assertEqual(collection.data, ["data_1", "data_2", "data_3"])

        # test caching data attribute
        self.assertEqual(collection.data, ["data_1", "data_2", "data_3"])
        self.assertEqual(collection.resolwe.data.filter.call_count, 1)

        # cache is cleared at update
        collection._data = ["data"]
        collection.update()
        self.assertEqual(collection._data, None)

        # raising error if collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.data

    def test_samples(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting samples attribute
        collection.resolwe.sample.filter = MagicMock(
            return_value=["sample1", "sample2"]
        )
        self.assertEqual(collection.samples, ["sample1", "sample2"])

        # cache is cleared at update
        collection._samples = ["sample"]
        collection.update()
        self.assertEqual(collection._samples, None)

        # raising error if data collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.samples

    def test_relations(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting relations attribute
        collection.resolwe.relation.filter = MagicMock(
            return_value=["relation1", "relation2"]
        )
        self.assertEqual(collection.relations, ["relation1", "relation2"])

        # cache is cleared at update
        collection._relations = ["relation"]
        collection.update()
        self.assertEqual(collection._relations, None)

        # raising error if data collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.relations


if __name__ == "__main__":
    unittest.main()
