# -*- coding: utf-8 -*-
"""
    Setup file for repo_name_to_be_changed.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys

from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

from src.zernike_simulation.viz.GenReport import GenReport
if __name__ == "__main__":
    setup(use_pyscaffold=True,
        cmdclass={'gen_report': GenReport})
