#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import poetry_version
from setuptools import setup

with open("requirements.txt") as f:
    REQUIRES = f.readlines()


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="chachacha",
    python_requires=">=3.6",
    version=poetry_version.extract(source_file=__file__),
    url="https://github.com/aogier/chachacha",
    license="BSD",
    description="Chachacha changes changelogs.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Alessandro Ogier",
    author_email="alessandro.ogier@gmail.com",
    packages=get_packages("chachacha"),
    install_requires=REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["chachacha=chachacha.main:main",]},
    zip_safe=False,
)
