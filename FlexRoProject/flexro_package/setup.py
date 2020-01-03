#!/usr/bin/env python2

from distutils.core import setup
from setuptools import find_packages
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*tests*"]),
    package_dir={'': 'src'}, )

setup(**setup_args)