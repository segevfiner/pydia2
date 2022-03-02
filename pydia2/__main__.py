"""
Dump debug information for executable or from a pdb.

This is a reproduction of the DIA2Dump sample included with the DIA SDK.
"""
# TODO Audit exception handling
import sys
import os
import argparse
import comtypes
import pydia2
from pydia2 import dia, cvconst

__package__ = "pydia2"


MAX_RVA_LINES_BYTES_RANGE = 0x100


def load_data_from_pdb(file):
    source = pydia2.CreateObject(dia.DiaSource, dia.IDiaDataSource)

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
    dump_all_globals(session)
    dump_all_types(session)
    dump_all_files(session)
    dump_all_lines(session)
    dump_all_sec_contribs(session)
    dump_all_debug_streams(session)
    dump_all_injected_sources(session)
    dump_all_fpo(session)
    dump_all_oems(session)


def dump_all_mods(session):
    print("\n\n*** MODULES\n")

    enum_symbols = session.globalScope.findChildren(cvconst.SymTag.Compiland, None, 0)
    for i, symbol in enumerate(enum_symbols, 1):
        symbol = symbol.QueryInterface(dia.IDiaSymbol)
        print(f"{i:04X} {symbol.name}")

    print()


def dump_all_publics(session):
    print("\n\n*** PUBLICS\n")

    enum_symbols = session.globalScope.findChildren(cvconst.SymTag.PublicSymbol, None, 0)
    for symbol in enum_symbols:
        symbol = symbol.QueryInterface(dia.IDiaSymbol)
        print_public_symbol(symbol)

    print()


def dump_all_symbols(session):
    print("\n\n*** SYMBOLS\n")

    enum_symbols = session.globalScope.findChildren(cvconst.SymTag.Compiland, None, 0)
    for compiland in enum_symbols:
        compiland = compiland.QueryInterface(dia.IDiaSymbol)
        print("\n** Module: ", end='')

        try:
            print(f"{compiland.name}\n")
        except comtypes.COMError:
            print("(???)\n")

        enum_children = compiland.findChildren(cvconst.SymTag.Null, None, 0)
        for symbol in enum_children:
            symbol = symbol.QueryInterface(dia.IDiaSymbol)
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

    print(f"{cvconst.SymTag(symbol.symTag).name}: [{rva:08X}][{symbol.addressSection:04X}:{symbol.addressOffset:08X}] ", end='')

    if symbol.symTag == cvconst.SymTag.Thunk:
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
    print("TODO", end='')  # TODO


def print_call_site_info(symbol):
    print("TODO", end='')  # TODO


def print_heap_alloc_site(symbol):
    print("TODO", end='')  # TODO


def print_coff_group(symbol):
    print("TODO", end='')  # TODO


def print_symbol(symbol, indent):
    try:
        sym_tag = symbol.symTag
    except comtypes.COMError:
        print("ERROR - PrintSymbol get_symTag() failed")

    if sym_tag == cvconst.SymTag.Function:
        print()

    print_sym_tag(sym_tag)

    print(' ' * indent, end='')

    if sym_tag == cvconst.SymTag.CompilandDetails:
        print_compiland_details(symbol)

    elif sym_tag == cvconst.SymTag.CompilandEnv:
        print_compiland_env(symbol)

    elif sym_tag == cvconst.SymTag.Data:
        print_data(symbol)

    elif sym_tag in (cvconst.SymTag.Function, cvconst.SymTag.Block):
        print_location(symbol)

        try:
            print(f", len = {symbol.length:08X}", end='')
        except comtypes.COMError:
            pass

        if sym_tag == cvconst.SymTag.Function:
            try:
                print(f", {cvconst.Call(symbol.callingConvention).name}", end='')
            except comtypes.COMError:
                pass

        print_und_name(symbol)
        print()

        if sym_tag == cvconst.SymTag.Function:
            print(' ' * indent, end='')
            print("                 Function attribute:", end='')

            try:
                if symbol.isCxxReturnUdt:
                    print(" return user defined type (C++ style)", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.constructor:
                    print(" instance constructor", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.isConstructorVirtualBase:
                    print(" instance constructor of a class with virtual base", end='')
            except comtypes.COMError:
                pass

            print()

            print(' ' * indent, end='')
            print("                 Function info:", end='')

            try:
                if symbol.hasAlloca:
                    print(" alloca", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasSetJump:
                    print(" setjmp", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasLongJump:
                    print(" longjmp", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasInlAsm:
                    print(" inlasm", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasEH:
                    print(" eh", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.inlSpec:
                    print(" inl_specified", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasSEH:
                    print(" seh", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.isNaked:
                    print(" naked", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasSecurityChecks:
                    print(" gschecks", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.isSafeBuffers:
                    print(" safebuffers", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.hasEHa:
                    print(" asyncheh", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.noStackOrdering:
                    print(" gsnostackordering", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.wasInlined:
                    print(" wasinlined", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.strictGSCheck:
                    print(" strict_gs_check", end='')
            except comtypes.COMError:
                pass

            print()

            enum_children = symbol.findChildren(cvconst.SymTag.Null, None, 0)
            for child in enum_children:
                child = child.QueryInterface(dia.IDiaSymbol)
                print_symbol(child, indent + 2)

    elif sym_tag == cvconst.SymTag.Annotation:
        print_location(symbol)
        print()

    elif sym_tag == cvconst.SymTag.Label:
        print_location(symbol)
        print(", ", end='')
        print_name(symbol)

    elif sym_tag in (cvconst.SymTag.Enum, cvconst.SymTag.Typedef, cvconst.SymTag.UDT, cvconst.SymTag.BaseClass):
        print_udt(symbol)

    elif sym_tag in (cvconst.SymTag.FuncDebugStart, cvconst.SymTag.FuncDebugEnd):
        print_location(symbol)

    elif sym_tag in (cvconst.SymTag.FunctionArgType, cvconst.SymTag.FunctionType, cvconst.SymTag.PointerType, cvconst.SymTag.ArrayType, cvconst.SymTag.BaseType):
        try:
            print_type(symbol.type)
        except comtypes.COMError:
            pass

        print()

    elif sym_tag == cvconst.SymTag.Thunk:
        print_thunk(symbol)

    elif sym_tag == cvconst.SymTag.CallSite:
        print_call_site_info(symbol)

    elif sym_tag == cvconst.SymTag.HeapAllocationSite:
        print_heap_alloc_site(symbol)

    elif sym_tag == cvconst.SymTag.CoffGroup:
        print_coff_group(symbol)

    else:
        print_name(symbol)

        try:
            type_ = symbol.type
            if type_:
                print(" has type ", end='')
                print_type(type_)
        except comtypes.COMError:
            pass

    if sym_tag in (cvconst.SymTag.UDT, cvconst.SymTag.Annotation):
        print()

        enum_children = symbol.findChildren(cvconst.SymTag.Null, None, 0)
        for child in enum_children:
            child = child.QueryInterface(dia.IDiaSymbol)
            print_symbol(child, indent + 2)

    print()


def print_sym_tag(sym_tag):
    print(f"{cvconst.SymTag(sym_tag).name:15s}: ", end='')


def print_name(symbol):
    try:
        name = symbol.name
    except comtypes.COError:
        print("(none)", end='')
        return

    try:
        undecorated_name = symbol.undecoratedName
    except comtypes.COMError:
        print(f"{name}", end='')
        return

    if undecorated_name is None or name == undecorated_name:
        print(f"{name}", end='')
    else:
        print(f"{undecorated_name}({name})")


def print_und_name(symbol):
    try:
        undecorated_name = symbol.undecoratedName
        if undecorated_name is not None and len(undecorated_name) > 0:
            print(f"{undecorated_name}", end='')
        else:
            print("(none)", end='')
    except comtypes.COMError:
        try:
            name = symbol.name
            if len(name) > 0:
                print(f"{name}", end='')
        except comtypes.Error:
            print("(none)", end='')


def print_thunk(symbol):
    try:
        print(f"[{symbol.relativeVirtualAddress:08X}][{symbol.addressSection:04X}:{symbol.addressOffset:08X}]", end='')
    except comtypes.COMError:
        pass

    try:
        print(f", target [{symbol.targetSection:08X}][{symbol.targetOffset:04X}:{symbol.targetRelativeVirtualAddress:08X}]", end='')
    except comtypes.COMError:
        print(", target ", end='')
        print_name(symbol)


def print_compiland_details(symbol):
    try:
        print(f"\n\tLanguage: {cvconst.CFL_LANG(symbol.language).name}")
    except comtypes.COMError:
        pass

    try:
        print(f"\tTarget processor: {cvconst.CPU_TYPE(symbol.platform).name}")
    except comtypes.COMError:
        pass

    try:
        if symbol.editAndContinueEnabled:
            print("\tCompiled for edit and continue: yes")
        else:
            print("\tCompiled for edit and continue: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.hasDebugInfo:
            print("\tCompiled without debugging info: no")
        else:
            print("\tCompiled without debugging info: yes")
    except comtypes.COMError:
        pass

    try:
        if symbol.isLTCG:
            print("\tCompiled with LTCG: yes")
        else:
            print("\tCompiled with LTCG: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.isDataAligned:
            print("\tCompiled with /bzalign: no")
        else:
            print("\tCompiled with /bzalign: yes")
    except comtypes.COMError:
        pass

    try:
        if symbol.hasManagedCode:
            print("\tManaged code present: yes")
        else:
            print("\tManaged code present: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.hasSecurityChecks:
            print("\tCompiled with /GS: yes")
        else:
            print("\tCompiled with /GS: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.isSdl:
            print("\tCompiled with /sdl: yes")
        else:
            print("\tCompiled with /sdl: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.isHotpatchable:
            print("\tCompiled with /hotpatch: yes")
        else:
            print("\tCompiled with /hotpatch: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.isCVTCIL:
            print("\tConverted by CVTCIL: yes")
        else:
            print("\tConverted by CVTCIL: no")
    except comtypes.COMError:
        pass

    try:
        if symbol.isMSILNetmodule:
            print("\tMSIL module: yes")
        else:
            print("\tMSIL module: no")
    except comtypes.COMError:
        pass

    try:
        print(f"\tFrontend Version: Major = {symbol.frontEndMajor}, Minor = {symbol.frontEndMinor}, build = {symbol.frontEndBuild}", end='')

        try:
            print(f", QFE = {symbol.frontEndQFE}", end='')
        except comtypes.COMError:
            pass

        print()
    except comtypes.COMError:
        pass

    try:
        print(f"\tBackend Version: Major = {symbol.backEndMajor}, Minor = {symbol.backEndMinor}, build = {symbol.backEndBuild}", end='')

        try:
            print(f", QFE = {symbol.backEndQFE}", end='')
        except comtypes.COMError:
            pass

        print()
    except comtypes.COMError:
        pass

    try:
        print(f"\tVersion string: {symbol.compilerName}", end='')
    except comtypes.COMError:
        pass

    print()


def print_compiland_env(symbol):
    print_name(symbol)
    print(" =", end='')
    print_variant(symbol.value)


def print_location(symbol):
    try:
        location_type = symbol.locationType
    except comtypes.COMError:
        print("symbol in optimized code", end='')
        return

    if location_type == cvconst.LocationType.Static:
        try:
            print(f"{cvconst.LocationType(location_type).name}, [{symbol.relativeVirtualAddress:08X}][{symbol.addressSection:04X}:{symbol.addressOffset:08X}]", end='')
        except comtypes.COMError:
            pass

    elif location_type in (cvconst.LocationType.TLS, cvconst.LocationType.LocInMetaData, cvconst.LocationType.IlRel):
        try:
            print(f"{cvconst.LocationType(location_type).name}, [{symbol.relativeVirtualAddress:08X}][{symbol.addressSection:04X}:{symbol.addressOffset:08X}]", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.RegRel:
        try:
            # TODO register names
            print(f"{symbol.registerId} Relative, [{symbol.offset:08X}]", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.ThisRel:
        try:
            print(f"this+0x{symbol.offset:X}", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.BitField:
        try:
            print(f"this(bf)+0x{symbol.offset:X}:0x{symbol.bitPosition:X} len(0x{symbol.length:X})", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.Enregistered:
        try:
            # TODO register names
            print(f"enregistered {symbol.registerId}", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.Slot:
        try:
            print(f"{cvconst.LocationType(location_type).name} {symbol.slot}", end='')
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.Constant:
        try:
            print(f"constant", end='')
            print_variant(symbol.value)
        except comtypes.COMError:
            pass

    elif location_type == cvconst.LocationType.Null:
        pass

    else:
        print(f"Error - invalid location type: 0x{location_type:X}", end='')


def print_const(symbol):
    print("TODO", end='')  # TODO


def print_udt(symbol):
    print_name(symbol)
    print_symbol_type(symbol)


def print_symbol_type(symbol):
    try:
        type_ = symbol.type
        print(", Type: ", end='')
        print_type(symbol)
    except comtypes.COMError:
        pass


def print_type(symbol):
    try:
        sym_tag = symbol.symTag
    except comtypes.COMError:
        print("ERROR - can't retrieve the symbol's SymTag")
        return

    try:
        name = symbol.name
    except comtypes.COMError:
        name = ''

    len_ = symbol.length

    if sym_tag != cvconst.SymTag.PointerType:
        try:
            if symbol.constType:
                print("const ", end='')
        except comtypes.COMError:
            pass

        try:
            if symbol.volatileType:
                print("volatile ", end='')
        except comtypes.COMError:
            pass

        try:
            if symbol.unalignedType:
                print("__unaligned ", end='')
        except comtypes.COMError:
            pass

        if sym_tag == cvconst.SymTag.UDT:
            print_udt_kind(symbol)
            print_name(symbol)

        elif sym_tag == cvconst.SymTag.Enum:
            print("enum ", end='')
            print_name(symbol)

        elif sym_tag == cvconst.SymTag.FunctionType:
            print("function ", end='')

        elif sym_tag == cvconst.SymTag.PointerType:
            try:
                base_type = symbol.type
            except comtypes.COMError:
                print("ERROR - SymTagPointerType get_type", end='')
                return

            print_type(base_type)

            try:
                if symbol.reference:
                    print(" &")
                else:
                    print(" *")
            except comtypes.COMError:
                pass

            try:
                if symbol.constType:
                    print("const ", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.volatileType:
                    print("volatile ", end='')
            except comtypes.COMError:
                pass

            try:
                if symbol.unalignedType:
                    print("__unaligned ", end='')
            except comtypes.COMError:
                pass


        elif sym_tag == cvconst.SymTag.ArrayType:
            try:
                base_type = symbol.type
            except comtypes.Error:
                print("ERROR - SymTagArrayType get_type")
                return

            print_type(base_type)

            try:
                rank = symbol.rank
                enum_sym = symbol.findChildren(cvconst.SymTag.Dimension, None, 0)
                for sym in enum_sym:
                    sym = sym.QueryInterface(dia.IDiaSymbol)

                    print("[", end='')

                    try:
                        print_bound(symbol.lowerBound)
                        print("..", end='')
                    except comtypes.COMError:
                        pass

                    try:
                        print_bound(symbol.upperBound)
                        print("..", end='')
                    except comtypes.COMError:
                        pass

                    print("]", end='')
            except comtypes.Error:
                enum_sym = symbol.findChildren(cvconst.SymTag.CustomType, None, 0)
                if enum_sym is not None and enum_sym.Count > 0:
                    for sym in enum_sym:
                        sym = sym.QueryInterface(dia.IDiaSymbol)
                        print("[", end='')
                        print_type(sym)
                        print("]", end='')
                else:
                    try:
                        print(f"[0x{symbol.count:X}", end='')
                    except comtypes.Error:
                        try:
                            len_array = symbol.length
                            len_elem = base_type.length

                            if len_elem == 0:
                                print(f"[0x{len_array:X}]", end='')
                            else:
                                print(f"[0x{len_array / len_elem}]", end='')

                        except comtypes.Error:
                            pass


        elif sym_tag == cvconst.SymTag.BaseType:
            try:
                info = symbol.baseType
            except comtypes.COMError:
                print("SymTagBaseType get_baseType", end='')
                return

            if info == cvconst.BasicType.UInt:
                print("unsigned ", end='')

            if info == cvconst.BasicType.Int:
                if len_ == 1:
                    if info == cvconst.BasicType.Int:
                        print("signed ", end='')

                elif len_ == 2:
                    print("short", end='')

                elif len_ == 4:
                    print("int", end='')

                elif len_ == 8:
                    print("__int64", end='')

                info = 0xFFFFFFFF

            elif info == cvconst.BasicType.Float:
                if len_ == 4:
                    print("float", end='')
                elif len_ == 8:
                    print("double", end='')

                info = 0xFFFFFFFF

            if info != 0xFFFFFFFF:
                # TODO Better strings?
                print(f"{cvconst.BasicType(info).name}", end='')


        elif sym_tag == cvconst.SymTag.Typedef:
            print_name(symbol)

        elif sym_tag == cvconst.SymTag.CustomType:
            pass  # TODO

        elif sym_tag == cvconst.SymTag.Data:
            print_location(symbol)


def print_bound(symbol):
    pass  # TODO


def print_data(symbol):
    print_location(symbol)

    print(f", {cvconst.DataKind(symbol.dataKind).name}", end='')
    print_symbol_type(symbol)

    print(", ", end='')
    print_name(symbol)


def print_variant(var):
    print("TODO", end='')  # TODO


def print_udt_kind(symbol):
    print("TODO", end='')  # TODO


def print_type_in_detail(symbol, indent):
    print("TODO", end='')  # TODO


def print_function_type(symbol):
    print("TODO", end='')  # TODO


def print_source_file(source):
    print("TODO", end='')  # TODO


def print_lines(session, function):
    print("TODO", end='')  # TODO


def print_enum_lines(lines):
    print("TODO", end='')  # TODO


def print_sec_contribs(segment):
    print("TODO", end='')  # TODO


def print_stream_data(stream):
    print("TODO", end='')  # TODO


def print_frame_data(frame_data):
    print("TODO", end='')  # TODO


def print_property_storage(prop_store):
    print("TODO", end='')  # TODO


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
