#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import os

REQUIRES = [
    'pandas',
    'numpy',
    'tqdm',
    'sklearn'
]

setup(
    name='wllutils',
    version='0.0.5',
    description=('utils of wll' ),
    # long_description=DESCRIPTION,
    # long_description_content_type='text/markdown',
    author='weiliulei',
    author_email='18500964455@163.com' ,
    maintainer='weiliulei',
    maintainer_email='18500964455@163.com' ,
    license = 'MIT',
    packages=find_packages(),
    platforms=['all',],
    url='https://github.com/Wei-Liulei/utils',
    install_requires=REQUIRES,
    # entry_points={
    #     'console_scripts': [CONSOLE_SCRIPT],
    # }
)

# pip install twine
# 打包 tar.gz ,whl,  windows 下 bdist_wininst
# python .\setup.py sdist bdist_wheel # bdist_wininst
# twine upload dist/*



