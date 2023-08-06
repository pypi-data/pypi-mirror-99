#!/usr/bin/env python3
"""
This module provides a set of functions to work with musical pitch. It enables
to convert between frequenies, midinotes and notenames
"""
from setuptools import setup

classifiers = """
"""

setup(name='pitchtools',
      version='1.0.0',
      description='Utilities to convert between midinotes, frequency and notenames', 
      long_description=__doc__,
      classifiers=list(filter(None, classifiers.split('\n'))),
      author='Eduardo Moguillansky',
      author_email='eduardo.moguillansky@gmail.com',
      py_modules=['pitchtools'],
      url="https://github.com/gesellkammer/pitchtools"
)


