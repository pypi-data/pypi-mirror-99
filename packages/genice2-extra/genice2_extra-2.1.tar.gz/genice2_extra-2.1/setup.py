#!/usr/bin/env python

# from distutils.core import setup, Extension
from setuptools import setup, Extension

long_desc = "".join(open("README.md").readlines())


setup(
    name='genice2_extra',
    version='2.1', # for genice2.1
    description='Installs all extra plugins for GenIce.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    url='https://github.com/vitroid/genice-extra/',
    keywords=['genice'],
    install_requires=['genice2-cage',         # 2.1 Compliant
                      # 'genice2-rdf',
                      'genice2-svg',          # 2.1 Compliant
                      'genice2-cif',          # 2.1 Compliant
                      # 'genice2-twist',
                      'genice2-mdanalysis',   # 2.1 compliant
                      ],

    license='MIT',
)

# genice-rdfはバグが解決していないので外す。mdanalysisを利用するのを推奨。
