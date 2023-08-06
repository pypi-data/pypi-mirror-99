# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Setup file for interpret-community package."""
from setuptools import setup, find_packages
import os

_major = "0.0"
_minor = "0"

if os.path.exists("../major.version"):
    with open("../major.version", "rt") as bf:
        _major = str(bf.read()).strip()

if os.path.exists("../minor.version"):
    with open("../minor.version", "rt") as bf:
        _minor = str(bf.read()).strip()

VERSION = "{}.{}".format(_major, _minor)
SELFVERSION = VERSION
if os.path.exists("patch.version"):
    with open("patch.version", "rt") as bf:
        _patch = str(bf.read()).strip()
        SELFVERSION = "{}.{}".format(VERSION, _patch)


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
]

DEPENDENCIES = [
    "interpret-community"
]

setup(
    name="erroranalysis",
    version=SELFVERSION,
    description="Microsoft Error Analysis SDK for Python",
    long_description="",  # README,
    long_description_content_type="text/markdown",
    author="Microsoft Corp",
    author_email="ilmat@microsoft.com",
    license="MIT License",
    url="https://docs.microsoft.com/en-us/azure/machine-learning/service/",
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["*.tests"]),
    install_requires=DEPENDENCIES,
    include_package_data=True,
    zip_safe=False,
)
