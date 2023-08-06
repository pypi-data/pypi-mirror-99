# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="fastutils",
    version="0.40.0",
    description="Collection of simple utils.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=[
        'fastutils',
        'aesutils',
        "cacheutils",
        "cipherutils",
        "dictutils",
        "fsutils",
        "funcutils",
        "hashutils",
        "httputils",
        "imageutils",
        "jsonutils",
        "listutils",
        "logutils",
        "nameutils",
        "numericutils"
        "pinyinutils",
        "randomutils",
        "rasutils",
        "strutils",
        "sysutils",
        "threadutils",
        "timeutils",
        "treeutils",
        "typingutils",
    ],
    install_requires=requires,
    packages=find_packages(".", exclude=["tests"]),
)