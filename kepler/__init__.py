# -*- coding: utf-8 -*-

"""Top-level package for Kepler."""
__author__ = """William Fong"""
__email__ = 'willfong@mit.edu'
__version__ = '0.0.1a'
import os

if os.name == 'nt':
    from .kepler import Kepler
else:
    from kepler.kepler import Kepler

__all__ = ['Kepler']
