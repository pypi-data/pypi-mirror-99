# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:30:30 2018

@author: shane
"""

import glob
import os
import shutil
import subprocess
import sys
import traceback

from setuptools import setup, find_packages

from ntclient import __version__

# Old pip doesn't respect `python_requires'
if sys.version_info < (3, 6, 5):
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python 3.6.5 or later to install")
    print("HINT:  You're running Python " + ver)
    exit(1)

# cd to parent dir of setup.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
shutil.rmtree("dist", True)

CLASSIFIERS = [
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Education",
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

REQUIREMENTS = [
    "argcomplete",
    "colorama",
    "fuzzywuzzy",
    "python-dotenv",
    "python-Levenshtein",
    "requests",
    "tabulate",
]

README = open("README.rst").read()

PKG_NAME = "nutra"

setup(
    name=PKG_NAME,
    author="gamesguru",
    author_email="mathmuncher11@gmail.com",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    python_requires=">=3.6.5",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    scripts=glob.glob("scripts/*"),
    # entry_points={"console_scripts": ["nutra=ntclient.__main__:main"]},
    description="Home and office nutrient tracking software",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/nutratech/cli",
    license="GPL v3",
    version=__version__,
)

# Clean up
shutil.rmtree(f"{PKG_NAME}.egg-info", True)
shutil.rmtree("__pycache__", True)
shutil.rmtree(".pytest_cache", True)
