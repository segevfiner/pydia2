pydia2
======
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

DIA (Debug Information Access) is distrbuted according to the Microsoft Visual Studio™ distributable
code license terms: https://visualstudio.microsoft.com/license-terms/mlt031819/
