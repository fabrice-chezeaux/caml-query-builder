# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Caml Query Builder'

with open("README.md", 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
        name="CamlQueryBuilder", 
        version=VERSION,
        author="Fabrice CHEZEAUX",
        author_email="<ifabrice.chezeaux@gmail.com>",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=['python', 'caml', 'sharepoint', 'rest', 'api', 'builder', 'query'],
        url = '',
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=find_packages(exclude=['tests'])
)