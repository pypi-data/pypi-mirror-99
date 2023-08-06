#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

depend_packages=[
        'gadgetron',
        'matplotlibqml',
        'PySide6',
]

setup(
    name='gadgetron-dataflow-monitor',
    version='0.95.001',
    description='Gadgetron Dataflow Monitor',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    install_requires=depend_packages,
    author='Cong Zhang',
    author_email='congzhangzh@gmail.com',
    maintainer='Cong Zhang',
    maintainer_email='congzhangzh@gmail.com',
    url='https://github.com/medlab/gadgetron-dataflow-monitor',
    packages=['gadm'],
    package_dir={'':'src'},
    package_data={'':['**/*.h5']},
    #data_files=['gadm/test_datas/testdata.h5'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)