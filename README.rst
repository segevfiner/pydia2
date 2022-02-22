pydia2
======
.. image:: https://img.shields.io/pypi/v/pydia2.svg
   :target: https://pypi.org/project/pydia2/
   :alt: PyPI

.. image:: https://github.com/segevfiner/pydia2/actions/workflows/docs.yml/badge.svg
   :target: https://segevfiner.github.io/pydia2/
   :alt: Docs

DIA packaged for use without COM registration using `comtypes <https://pypi.org/project/comtypes/>`_.

Installation
------------
Wheels are available. Building from source requires the DIA SDK (Install the "Desktop development
with C++" workload of Visual Studio).

.. code-block:: sh

    pip install pydia2

Example
-------
.. code-block:: python

    import pydia2

    source = pydia2.CreateObject(pydia2.dia.DiaSource, interface=pydia2.dia.IDiaDataSource)
    source.loadDataFromPdb("example.pdb")
    session = source.openSession()

    # Query the session...

License
-------
MIT license.

DIA (Debug Information Access) is distributed according to the Microsoft Visual Studio™ distributable
code license terms: https://visualstudio.microsoft.com/license-terms/mlt031819/
