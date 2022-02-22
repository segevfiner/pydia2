import sys
import os
import subprocess
import shutil
from setuptools import setup, find_packages, Extension



result = subprocess.run([
    os.path.expandvars(R"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"),
    '-latest',
    '-requires', 'Microsoft.VisualCpp.DIA.SDK',
    '-find', 'DIA SDK'],
    stdout=subprocess.PIPE,
    text=True)
result.check_returncode()
dia_sdk = result.stdout.strip()


if sys.maxsize > 2**32 - 1:
    arch_dir = "amd64"
else:
    arch_dir = ""


if not os.path.exists("pydia2/lib/x86/msdia140.dll"):
    shutil.copy(os.path.join(dia_sdk, "bin/msdia140.dll"), "pydia2/lib/x86/msdia140.dll")


if not os.path.exists("pydia2/lib/amd64/msdia140.dll"):
    shutil.copy(os.path.join(dia_sdk, "bin/amd64/msdia140.dll"), "pydia2/lib/amd64/msdia140.dll")


setup(
    name="pydia2",
    version="0.1.0",
    packages=find_packages(),
    ext_modules=[
        Extension(
            "pydia2._dia", ["pydia2/_dia.cpp"],
            include_dirs=[os.path.join(dia_sdk, "include")],
            library_dirs=[os.path.join(dia_sdk, "lib", arch_dir)],
            libraries=["Advapi32", "diaguids"],
        ),
    ],
    zip_safe=False,
    install_requires=[
        "comtypes",
    ]
)
