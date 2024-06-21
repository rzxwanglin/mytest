# -*-coding:utf-8 -*-
"""
# File       : setup.py.py
# Time       ：2023/2/24 14:18
# Author     ：caomengqi
# version    ：python 3.6
"""
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='crypt',
    ext_modules=cythonize("crypt.py"),
)