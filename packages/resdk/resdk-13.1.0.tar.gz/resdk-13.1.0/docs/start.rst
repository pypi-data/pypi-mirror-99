.. _tutorial:

===============
Getting started
===============

This tutorial is for bioinformaticians. It will help you install the ReSDK and
explain some basic commands. We will connect to an instance of `Genialis
server`_, do some basic queries, and align raw reads to a genome.

.. _Genialis server: https://app.genialis.com

Installation
============

Installing is easy, just make sure you have Python_ and pip_ installed on your
computer. Run this command in the terminal (CMD on Windows)::

  pip install resdk

.. _Python: https://www.python.org/downloads/
.. _pip: https://pip.pypa.io/en/stable/installing/

.. TODO: Remove this warning when not needed anymore: Miha, Domen is this still relevant?

.. warning::

   If you use macOS, be aware that the version of `Python shipped with the
   system doesn't support TLSv1.2`_, which is required for connecting to
   any Genialis Server (and probably others). To solve the issue,
   install the latest version of Python 3.6+ `via the official
   installer from Python.org`_ or `with Homebrew`_.

.. _`Python shipped with the system doesn't support TLSv1.2`:
    http://pyfound.blogspot.si/2017/01/time-to-upgrade-your-python-tls-v12.html
.. _`via the official installer from Python.org`:
    https://www.python.org/downloads/mac-osx/
.. _`with Homebrew`:
    http://docs.python-guide.org/en/latest/starting/install/osx/

Registration
============

The examples presented here require access to a public `Genialis Server`_
that is configured for the examples in this tutorial. Some parts of the
documentation will work for registered users only. Please `request a Demo`_
on Genialis Server before you continue, and remember your username and
password.

.. _`Genialis Server`: https://app.genialis.com
.. _`request a Demo`: http://genial.is/Demo-Request

Connect to Genialis Server
==========================

Start the Python interpreter by typing ``python`` into the command line. You'll
recognize the interpreter by '>>>'. Now we can connect to the Genialis Server:

.. literalinclude:: files/start.py
  :lines: 2-9

.. note::

  If you omit the ``login()`` line you will be logged as anonymus user.
  Note that anonymus users do not have access to the ful set of features.

.. note::

	When connecting to the server through an interactive session, we suggest you
	use the ``resdk.start_logging()`` command. This allows you to see important
	messages (*e.g.* warnings and errors) when executing commands.

.. note::

  To avoid copy-pasting of the commands, you can
  :download:`download all the code <files/start.py>` used in this section.

Query data
==========

Before we start querying data on the server we should become familiar with what
a data object is. Everything that is uploaded or created (via processes) on a
server is a data object. The data object contains a complete record of the
processing that has occurred. It stores the inputs (files, arguments,
parameters...), the process (the algorithm) and the outputs (files, images,
numbers...). Let's retrieve all data objects from the server:

.. literalinclude:: files/start.py
  :lines: 11

This is all of the data on the server you have permissions for. As a new
user you can only see a small subset of all data objects. We can see the
data objects are referenced by *id*, *slug*, and *name*.

.. note::

	``id`` is the auto-generated **unique identifier** of an object. IDs are
	integers.

	``slug`` is the **unique name** of an object. The slug is automatically
	created from the ``name`` but can also be edited by the user. Only lowercase
	letters, numbers and dashes are allowed (will not accept white space or
	uppercase letters).

	``name`` is an arbitrary, **non unique name** of an object.

Let's say we now want to find some genomes. We don't always know the *id*,
*slug*, or *name* by heart, but we can use `filters`_ to find them. We will
query for all genome data objects:

.. _filters: http://resdk.readthedocs.io/en/latest/ref.html#resdk.ResolweQuery

.. literalinclude:: files/start.py
  :lines: 13

There are several unrelated data objects that pass through our filter. We can
filter the data even further, this time trying to find a genome in a FASTA
format:

.. literalinclude:: files/start.py
  :lines: 15

For future work we want to get the genome with a specific slug. We will `get`_
it and store a reference to it for later:

.. _get: http://resdk.readthedocs.io/en/latest/ref.html#resdk.ResolweQuery.get

.. literalinclude:: files/start.py
  :lines: 17,18

We have now seen how to use filters to find and get what we want. Let's
query and get a paired-end FASTQ data object:

.. literalinclude:: files/start.py
  :lines: 20-24

We now have ``genome`` and ``reads`` data objects. We can learn about an object
by calling certain object attributes. We can find out who created the object:

.. literalinclude:: files/start.py
  :lines: 26

and inspect the list of files it contains:

.. literalinclude:: files/start.py
  :lines: 28

These and many other data object attributes/methods are described `here`_.

.. _here: http://resdk.readthedocs.io/en/latest/ref.html#resdk.resources.Data

Run alignment
=============

A common analysis in bioinformatics is to align sequencing reads to a reference
genome. This is done by running a certain *process*. A process uses an
algorithm or a sequence of algorithms to turn given inputs into outputs. Here
we will only test the HISAT2 alignment process, but many more processes are
available (see the `Process catalog`_). This process automatically creates a
BAM alignment file and BAI index, along with some other files.

.. _Process catalog: http://resolwe-bio.readthedocs.io/en/latest/catalog.html

Let's run HISAT2 on our reads, using our genome:

.. literalinclude:: files/start.py
  :lines: 30-36

This might seem like a complicated statement, but note that we only run a
process with specific slug and required inputs. The processing may take some
time. Note that we have stored the reference to the alignment object in a
``bam`` variable. We can check the `status`_ of the process to determine if
the processing has finished:

.. _status: http://resdk.readthedocs.io/en/latest/ref.html#resdk.resources.Data.status

.. literalinclude:: files/start.py
  :lines: 38

Status ``OK`` indicates that processing has finished successfully. If the
status is not ``OK`` yet, run the ``bam.update()`` and ``bam.status`` commands
again in few minutes. We can inspect our newly created data object:

.. literalinclude:: files/start.py
  :lines: 40-42

As with any other data object, it has its own *id*, *slug*, and *name*. We can
explore the process inputs and outputs:

.. literalinclude:: files/start.py
  :lines: 44-48

Download the outputs to your local disk:

.. literalinclude:: files/start.py
  :lines: 50

We have come to the end of Getting started. You now know some basic ReSDK
concepts and commands. Yet, we have only scratched the surface. By continuing
with the Tutorials, you will become familiar with more advanced features, and
will soon be able to perform powerful analyses on your data.
