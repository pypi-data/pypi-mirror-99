#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from os import path

here = path.abspath(path.dirname(__file__))
try:
    with open(path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = ""

setup(
    name='package-fib',
    packages=find_packages(),
    version='1.0.0',
    description='Fibonacci calculation',
    long_description=long_description,
    author='Pablo Henrique',
    author_email='ph.info.cont@rede.ulbra.br',
    url='',
    install_requires=[],
    license='MIT',
    keywords=['dev'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)