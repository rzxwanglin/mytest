# -*-coding:utf-8 -*-
"""
# File       : setup.py.py
# Time       ：2023/5/18 10:59
# Author     ：caomengqi
# version    ：python 3.6
"""
from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="rhino_v2_utilis",
    version="0.1.0",
    author="caomengqi",
    author_email="",
    description="封装爬虫中常用模块",
    url="",  # github地址或其他地址
    packages=["rhino_v2_utilis"],
    include_package_data=True,
    install_requires=[
        "redisbloom==0.4.1",  # 所需要包的版本号
        "redis==3.5.3",
        "loguru==0.6.0",  # 所需要包的版本号  # 所需要包的版本号
    ],
    zip_safe=True,
)
