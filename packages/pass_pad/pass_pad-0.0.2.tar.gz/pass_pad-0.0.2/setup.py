####
#####!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pass_pad',
    version='0.0.2',
    author='prgrmz07',
    author_email='prgrmz07@163.com',
    url='https://blog.csdn.net/hfcaoguilin',
    description=u'pass_pad',
    packages=['pass_pad'],
    install_requires=[
        'pycryptodomex>=3.10.1',
        'pandas>=1.1.3'
    ],
    entry_points={
        'console_scripts': [
            'pass_pad=pass_pad:main',
            # 'pass_pad_test=pass_pad:test'
        ]
    }
)