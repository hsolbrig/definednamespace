#!/usr/bin/env python
import sys

from setuptools import setup

if sys.version_info < (3, 5):
    raise Exception("Python 3.5 or higher is required. Your version is %s." % sys.version)

setup(
    setup_requires=['pbr'],
    pbr=True,
)
