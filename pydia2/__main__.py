"""
Dump debug information for executable or from a pdb.

This is a reproduction of the DIA2Dump sample included with the DIA SDK.
"""
import sys
import os
import argparse
import comtypes
import pydia2

__package__ = "pydia2"


def load_data_from_pdb(file):
    source = pydia2.CreateObject(pydia2.dia.DiaSource, pydia2.dia.IDiaDataSource)

    if os.path.splitext(file)[1] == ".pdb":
        source.loadDataFromPdb(file)
    else:
        # TODO Add callback?
        source.loadDataForExe(file, None, None)

    session = source.openSession()

    return (source, session)


def dump_all_pdb_info(session):
    dump_all_mods(session)
    dump_all_publics(session)
    dump_all_symbols(session)


def dump_all_mods(session):
    print("\n\n*** MODULES\n")

    enum_symbols = session.globalScope.findChildren(pydia2.dia.SymTagCompiland, None, 0)

    for i, symbol in enumerate(enum_symbols, 1):
        symbol = symbol.QueryInterface(pydia2.dia.IDiaSymbol)
        print(f"{i:04X} {symbol.name}")

    print()


def print_public_symbol(symbol):
    try:
        rva = symbol.relativeVirtualAddress
    except comtypes.COMError:
        rva = 0xFFFFFFFF

    print(f"{pydia2.SymTag(symbol.symTag).name}: [{rva:08X}][{symbol.addressSection:04X}:{symbol.addressOffset:08X}] ", end='')

    if symbol.symTag == pydia2.dia.SymTagThunk:
        try:
            print("f{symbol.name}")
        except comtypes.COMError:
            try:
                target_rva = symbol.targetRelativeVirtualAdddress
            except comtypes.COMError:
                target_rva = 0xFFFFFFFF

            print(f"target -> [{target_rva:08X}][{symbol.targetSection:04X}:{symbol.targetOffset:08X}]")
    else:
        try:
            print(f"{symbol.name}({symbol.undecoratedName})")
        except comtypes.COMError:
            print(f"{symbol.name}")


def dump_all_publics(session):
    print("\n\n*** PUBLICS\n")

    enum_symbols = session.globalScope.findChildren(pydia2.dia.SymTagPublicSymbol, None, 0)

    for symbol in enum_symbols:
        symbol = symbol.QueryInterface(pydia2.dia.IDiaSymbol)
        print_public_symbol(symbol)

    print()


def dump_all_symbols(session):
    pass


def main():
    parser = argparse.ArgumentParser(prog="pydia2", description=__doc__)
    parser.add_argument("file")
    parser.add_argument("-a", "--all", action="store_true", help="print all the debug info")
    parser.add_argument("-m", "--mods", action="store_true", help="print all the mods")
    parser.add_argument("-p", "--publics", action="store_true", help="print all the publics")
    parser.add_argument("-s", "--symbols", action="store_true", help="print symbols")

    args = parser.parse_args()

    source, session = load_data_from_pdb(args.file)

    if args.all:
        dump_all_pdb_info(session)
        return

    if args.mods:
        dump_all_mods(session)

    if args.publics:
        dump_all_publics(session)

    if args.symbols:
        dump_all_symbols(session)


if __name__ == "__main__":
    sys.exit(main())
