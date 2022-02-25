"""
DIA packaged for use without COM registration using comtypes.
"""

import sys
import pathlib
import ctypes
import enum
import comtypes
from comtypes import client
from . import _dia, cvconst


__version__ = "0.1.0"


_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

if sys.maxsize > 2**32 - 1:
    _arch = "amd64"
else:
    _arch = "x86"

_DIA_DLL = _SCRIPT_DIR / 'lib' / _arch / "msdia140.dll"


#: The dia typelib module. Retrieved via :func:`comtypes.client.GetModule`.
#:
#: :meta hide-value:
dia = client.GetModule(str(_DIA_DLL))


_NoRegCoCreate = ctypes.WINFUNCTYPE(
    ctypes.HRESULT,
    ctypes.c_wchar_p,
    ctypes.POINTER(comtypes.GUID),
    ctypes.POINTER(comtypes.GUID),
    ctypes.POINTER(ctypes.c_void_p),

)(_dia.NoRegCoCreatePtr)


def CreateObject(progid, interface=None):
    """
    Create a DIA object from *progid* with the given *interface*.

    Since this is intended to be used without registering DIA, you should grab the progid as a class
    object from the :data:`dia` module variable.
    """
    if interface is None:
        interface = comtypes.IUnknown

    clsid = comtypes.GUID.from_progid(progid)
    p = ctypes.POINTER(interface)()
    iid = interface._iid_
    _NoRegCoCreate(str(_DIA_DLL), ctypes.byref(clsid), ctypes.byref(iid), ctypes.byref(p))
    return client.GetBestInterface(p)
