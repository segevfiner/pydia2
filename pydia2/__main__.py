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


MAX_RVA_LINES_BYTES_RANGE = 0x100


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


def dump_all_publics(session):
    print("\n\n*** PUBLICS\n")

    enum_symbols = session.globalScope.findChildren(pydia2.dia.SymTagPublicSymbol, None, 0)
    for symbol in enum_symbols:
        symbol = symbol.QueryInterface(pydia2.dia.IDiaSymbol)
        print_public_symbol(symbol)

    print()


def dump_all_symbols(session):
    print("\n\n*** SYMBOLS\n")

    enum_symbols = session.globalScope.findChildren(pydia2.dia.SymTagCompiland, None, 0)
    for compiland in enum_symbols:
        compiland = compiland.QueryInterface(pydia2.dia.IDiaSymbol)
        print("\n** Module: ", end='')

        try:
            print(f"{compiland.name}\n")
        except comtypes.COMError:
            print("(???)\n")

        enum_children = compiland.findChildren(pydia2.dia.SymTagNull, None, 0)
        for symbol in enum_children:
            symbol = symbol.QueryInterface(pydia2.dia.IDiaSymbol)
            print_symbol(symbol, 0)

    print()


def dump_all_globals(session):
    pass  # TODO


def dump_all_types(session):
    pass  # TODO


def dump_all_udts(session):
    pass  # TODO


def dump_all_enums(session):
    pass  # TODO


def dump_all_typedefs(session):
    pass  # TODO


def dump_all_files(session):
    pass  # TODO


def dump_all_lines(session):
    pass  # TODO


def dump_all_lines_at_rva(session):
    pass  # TODO


def dump_all_sec_contribs(session):
    pass  # TODO


def dump_all_debug_streams(session):
    pass  # TODO


def dump_all_injected_sources(session):
    pass  # TODO


def dump_injected_source(session, name):
    pass  # TODO


def dump_all_sources_files(session):
    pass  # TODO


def dump_all_fpo(session):
    pass  # TODO


def dump_all_oems(session):
    pass  # TODO


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


def print_global_symbol(symbol):
    pass  # TODO


def print_call_site_info(symbol):
    pass  # TODO


def print_heap_alloc_site(symbol):
    pass  # TODO


def print_coff_group(symbol):
    pass  # TODO


def print_symbol(symbol, indent):
    try:
        sym_tag = symbol.symTag
    except comtypes.COMError:
        print("ERROR - PrintSymbol get_symTag() failed")

    if sym_tag == pydia2.dia.SymTagFunction:
        print()

    print_sym_tag(sym_tag)

    print(' ' * indent, end='')

    if sym_tag == pydia2.dia.SymTagCompilandDetails:
        print_compiland_details(symbol)

    elif sym_tag == pydia2.dia.SymTagCompilandEnv:
        print_compiland_env(symbol)

    elif sym_tag == pydia2.dia.SymTagData:
        print_data(symbol)

    elif sym_tag in (pydia2.dia.SymTagFunction, pydia2.dia.SymTagBlock):
        print_location(symbol)

        # TODO
    elif sym_tag == pydia2.dia.SymTagAnnotation:
        print_location(symbol)
        print()

    elif sym_tag == pydia2.dia.SymTagLabel:
        print_location(symbol)
        print(", ", end='')
        print_name(symbol)

    elif sym_tag in (pydia2.dia.SymTagEnum, pydia2.dia.SymTagTypedef, pydia2.dia.SymTagUDT, pydia2.dia.SymTagBaseClass):
        print_udt(symbol)

    elif sym_tag in (pydia2.dia.SymTagFuncDebugStart, pydia2.dia.SymTagFuncDebugEnd):
        print_location(symbol)

    elif sym_tag in (pydia2.dia.SymTagFunctionArgType, pydia2.dia.SymTagFunctionType, pydia2.dia.SymTagPointerType, pydia2.dia.SymTagArrayType, pydia2.dia.SymTagBaseType):
        try:
            print_type(symbol.type)
        except comtypes.COMError:
            pass

        print()

    elif sym_tag == pydia2.dia.SymTagThunk:
        print_thunk(symbol)

    elif sym_tag == pydia2.dia.SymTagCallSite:
        print_call_site_info(symbol)

    elif sym_tag == pydia2.dia.SymTagHeapAllocationSite:
        print_heap_alloc_site(symbol)

    elif sym_tag == pydia2.dia.SymTagCoffGroup:
        print_coff_group(symbol)

    else:
        print_name(symbol)

        try:
            type_ = symbol.type
            print(" has type ")
            print_type(type_)
        except comtypes.COMError:
            pass


def print_sym_tag(sym_tag):
    print(f"{pydia2.SymTag(sym_tag).name:15s}: ", end='')


def print_name(symbol):
    pass  # TODO


def print_und_name(symbol):
    pass  # TODO


def print_thunk(symbol):
    pass  # TODO


def print_compiland_details(symbol):
    pass  # TODO


def print_compiland_env(symbol):
    pass  # TODO


def print_location(symbol):
    pass  # TODO


def print_const(symbol):
    pass  # TODO


def print_udt(symbol):
    pass  # TODO


def print_symbol_type(symbol):
    pass  # TODO


def print_type(symbol):
    pass  # TODO


def print_bound(symbol):
    pass  # TODO


def print_data(symbol):
    pass  # TODO


def print_variant(var):
    pass  # TODO


def print_udt_kind(symbol):
    pass  # TODO


def print_type_in_detail(symbol, indent):
    pass  # TODO


def print_function_type(symbol):
    pass  # TODO


def print_source_file(source):
    pass  # TODO


def print_lines(session, function):
    pass  # TODO


def print_enum_lines(lines):
    pass  # TODO


def print_sec_contribs(segment):
    pass  # TODO


def print_stream_data(stream):
    pass  # TODO


def print_frame_data(frame_data):
    pass  # TODO


def print_property_storage(prop_store):
    pass  # TODO


def main():
    parser = argparse.ArgumentParser(prog="pydia2", description=__doc__)
    parser.add_argument("file")
    parser.add_argument("-a", "--all", action="store_true", help="print all the debug info")
    parser.add_argument("-m", "--mods", action="store_true", help="print all the mods")
    parser.add_argument("-p", "--publics", action="store_true", help="print all the publics")
    parser.add_argument("-g", "--globals", action="store_true", help="print all the globals")
    parser.add_argument("-t", "--types", action="store_true", help="print all the types")
    parser.add_argument("-f", "--files", action="store_true", help="print all the files")
    parser.add_argument("-s", "--symbols", action="store_true", help="print symbols")
    parser.add_argument("-l", nargs='?', metavar="RVA[:BYTES]", const=True, help="print line number info at RVA address in the bytes range")
    parser.add_argument("-c", "--sec-contribs", action="store_true", help="print section contribution info")
    parser.add_argument("--dbg", action="store_true", help="dump debug streams")
    parser.add_argument("--injsrc", nargs='?', metavar="FILE", const=True, help="dump injected source")
    parser.add_argument("--source-files", "--sf", action="store_true", help="dump all source files")
    parser.add_argument("--oem", action="store_true", help="dump all OEM specific types")
    parser.add_argument("--fpo", nargs='?', metavar="RVA/SYMBOL", const=True, help="dump frame pointer omission information for a func addr/symbol")
    parser.add_argument("--compiland", nargs='?', metavar="NAME", help="dump symbols for this compiland")
    parser.add_argument("--lines", metavar="RVA/FUNC", help="dump line numbers for this address/function")
    parser.add_argument("--type", metavar="SYMBOL", help="dump this type in detail")
    parser.add_argument("--label", metavar="RVA", help="dump label at RVA")
    parser.add_argument("--sym", metavar="SYMBOL/RVA[:CHILDNAME]", help="dump child information of this symbol/at this addr")
    parser.add_argument("--lsrc", metavar="FILE[:LINE]", help="dump line numbers for this source file")
    parser.add_argument("--ps", metavar="RVA", help="dump symbols after this address")
    parser.add_argument("--psr", metavar="RVA", help="dump symbols before this address")
    parser.add_argument("-n", type=int, default=16, help="number of symbols to dump for --ps/--psr")
    parser.add_argument("--annotations", metavar="RVA", help="dump annotation symbol for this RVA")
    parser.add_argument("--maptosrc", metavar="RVA", help="dump src RVA for this image RVA")
    parser.add_argument("--mapfromsrc", metavar="RVA", help="dump image RVA for src RVA")

    args = parser.parse_args()
    print(args)

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

    if args.globals:
        dump_all_globals(session)

    if args.types:
        dump_all_types(session)

    if args.files:
        dump_all_files(session)

    if args.l:
        if isinstance(args.l, str) and args.l != '-':
            rva, range = args.l.partition(":")
            rva = int(rva, 16)
            range = int(range) if range else MAX_RVA_LINES_BYTES_RANGE

            dump_all_lines_at_rva(session, rva)

        else:
            dump_all_lines(session)

    if args.sec_contribs:
        dump_all_sec_contribs(session)

    if args.dbg:
        dump_all_debug_streams(session)

    if args.injsrc:
        if isinstance(args.injsrc, str) and args.injsrc != '-':
            dump_injected_source(session, args.injsrc)
        else:
            dump_all_injected_sources(session)

    if args.source_files:
        dump_all_sources_files(session)

    if args.oem:
        dump_all_oems(session)

    if args.fpo:
        pass  # TODO

    if args.compiland:
        pass  # TODO

    if args.lines:
        pass  # TODO

    if args.type:
        pass  # TODO

    if args.label:
        pass  # TODO

    if args.sym:
        pass  # TODO

    if args.lsrc:
        pass  # TODO

    if args.ps:
        pass  # TODO

    if args.psr:
        pass  # TODO

    if args.annotations:
        pass  # TODO

    if args.maptosrc:
        pass  # TODO

    if args.mapfromsrc:
        pass  # TODO



if __name__ == "__main__":
    sys.exit(main())
