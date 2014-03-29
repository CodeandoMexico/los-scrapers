#!/usr/bin/env python

import setuptools

setuptools.setup(
    setup_requires=['d2to1'],
    d2to1=True,
    install_requires=[
        "requests",
        "pymongo"
    ]
)
