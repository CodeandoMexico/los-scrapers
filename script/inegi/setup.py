#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from .distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    setup_requires=['d2to1'],
    d2to1=True,
    install_requires=[
        "requests",
        "pymongo"
    ],
    entry_points={
        'console_scripts': [
            'inegi_get_data = inegi.inegi_get_data:get_data',
            'inegi_nosql = inegi.inegi_nosql:main',
            'inegi_sql = inegi.inegi_sql:main'
        ]
    }
)
