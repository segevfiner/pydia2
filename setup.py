import sys
import os
import re
import subprocess
import shutil
from setuptools import setup, find_packages, Extension


with open("pydia2/__init__.py", "r", encoding="utf-8") as f:
    version = re.search(r'(?m)^__version__ = "([a-zA-Z0-9.-]+)"', f.read()).group(1)

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()



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
    version=version,
    author="Segev Finer",
    author_email="segev208@gmail.com",
    description="DIA packaged for use without COM registration using comtypes",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/segevfiner/pydia2",
    project_urls={
        "Documentation": "https://segevfiner.github.io/pydia2/",
        "Issue Tracker": "https://github.com/segevfiner/pydia2/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["dia", "comtypes"],
    packages=find_packages(),
    ext_modules=[
        Extension(
            "pydia2._dia", ["pydia2/_dia.cpp"],
            include_dirs=[os.path.join(dia_sdk, "include")],
            library_dirs=[os.path.join(dia_sdk, "lib", arch_dir)],
            libraries=["Advapi32", "diaguids"],
            define_macros=[("Py_LIMITED_API", "0x03070000")],
            py_limited_api=True,
        ),
    ],
    package_data={
        "pydia2": ["lib/x86/msdia140.dll", "lib/amd64/msdia140.dll"],
    },
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "comtypes",
    ],
    extras_require={
        "dev": {
            "pycparser",
            "sphinx",
        }
    },
)
