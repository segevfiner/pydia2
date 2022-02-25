import sys
import os
import pathlib
import subprocess
from unicodedata import name
from pycparser import parse_file, c_ast, c_generator


_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


DEFS = {
    'CV_call_e': {
        'name': 'Call',
        'rmprefix': 'CV_CALL_',
    },
    'CV_access_e': {
        'name': 'Access',
        'rmprefix': 'CV_',
    },
    'THUNK_ORDINAL': {
        'rmprefix': 'THUNK_ORDINAL_',
    },
    'CV_SourceChksum_t': {
        'name': 'SourceChksum',
        'rmprefix': 'CHKSUM_TYPE_',
    },
    'SymTagEnum': {
        'name': 'SymTag',
        'rmprefix': 'SymTag',
    },
    'LocationType': {
        'rmprefix': 'LocIs',
    },
    'DataKind': {
        'rmprefix': 'DataIs',
    },
    'UdtKind': {
        'rmprefix': 'Udt',
    },
    'BasicType': {
        'rmprefix': 'bt',
    },
    'CV_modifier_e': {
        'name': 'Modifier',
        'rmprefix': 'CV_MOD_'
    },
    'CV_builtin_e': {
        'name': 'Builtin',
        'rmprefix': 'CV_BI_',
    },
    'CV_CFL_LANG': {
        'name': 'CFL_LANG',
        'rmprefix': 'CV_CFL_',
    },
    'CV_CPU_TYPE_e': {
        'name': 'CPU_TYPE',
        'rmprefix': 'CV_',
    },
    'CV_HREG_e': {
        'name': 'HREG',
        'rmprefix': 'CV_',
    },
    'CV_HLSLREG_e': {
        'name': 'HLSLREG',
        'rmprefix': 'CV_',
    },
    'StackFrameTypeEnum': {
        'name': 'StackFrameType',
        'rmprefix': 'FrameType',
    },
    'MemoryTypeEnum': {
        'name': 'MemoryType',
        'rmprefix': 'MemType',
    },
    'CV_HLSLMemorySpace_e': {
        'name': 'HLSLMemorySpace',
        'rmprefix': 'CV_HLSL_MEMSPACE_',
    },
    'NameHashBuild': {
        'rmprefix': 'NAMEHASH_BUILD_',
    },
    'CV_CoroutineKind_e': {
        'name': 'CoroutineKind',
        'rmprefix': 'CV_COROUTINEKIND_',
    },
    'CV_AssociationKind_e': {
        'name': 'AssociationKind',
        'rmprefix': 'CV_ASSOCIATIONKIND_',
    },
}


class EnumVisitor(c_ast.NodeVisitor):
    def __init__(self, output):
        super().__init__()
        self.output = output

    def visit_Enum(self, node):
        if node.name is None:
            if node.values.enumerators[0].name == "NAMEHASH_BUILD_START":
                name = "NameHashBuild"
            else:
                raise ValueError("enum with no name")
        else:
            name = node.name

        enum_def = DEFS.get(name, {})
        name = enum_def.get('name', name)
        rmprefix = enum_def.get('rmprefix', '')

        self.output.write(f"class {name}(IntEnum):\n")

        for i, enumerator in enumerate(node.values):
            if enumerator.value is not None:
                if isinstance(enumerator.value, c_ast.ID):
                    value = enumerator.value.name
                    if value.startswith(rmprefix):
                        value = value[len(rmprefix):]
                else:
                    generator = c_generator.CGenerator()
                    value = generator.visit(enumerator.value)
            else:
                if i == 0:
                    value = 0
                else:
                    value = 'auto()'

            enumerator_name = enumerator.name
            if enumerator_name.startswith(rmprefix):
                enumerator_name = enumerator_name[len(rmprefix):]

            self.output.write(f"    {enumerator_name} = {value}\n")

        self.output.write("\n\n")


def main():
    result = subprocess.run([
        os.path.expandvars(R"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"),
        '-latest',
        '-requires', 'Microsoft.VisualCpp.DIA.SDK',
        '-find', 'DIA SDK'],
        stdout=subprocess.PIPE,
        text=True)
    result.check_returncode()
    dia_sdk = pathlib.Path(result.stdout.strip())

    ast = parse_file(dia_sdk / 'include/cvconst.h', use_cpp=True, cpp_path='cl', cpp_args='/E')

    with open(_SCRIPT_DIR / "../pydia2/cvconst.py", "w") as f:
        f.write("from enum import IntEnum, auto\n\n\n")

        v = EnumVisitor(f)
        v.visit(ast)


if __name__ == "__main__":
    sys.exit(main())
