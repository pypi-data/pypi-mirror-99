#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='PIDController',
    version='0.0.1',
    author='xiaochuan',
    author_email='lixiaochuan822@gmail.com',
    description=u'PIDController',
    packages=['controller'],
    install_requires=['matplotlib', 'numpy'],
    entry_points={
        'console_scripts': [
            'sayit=controller:sayit',
        ]
    }
)