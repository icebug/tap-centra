#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

setup(
    name="tap-centra",
    version="0.0.1",
    description="Singer.io tap for extracting data from the Centra API",
    author="Smartr",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_centra"],
    install_requires=["tap-framework==0.0.4"],
    entry_points="""
          [console_scripts]
          tap-centra=tap_centra:main
      """,
    packages=find_packages(),
    package_data={"tap_centra": ["schemas/*.json"]},
)