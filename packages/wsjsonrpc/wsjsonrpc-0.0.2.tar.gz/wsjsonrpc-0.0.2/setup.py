#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools

basedir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(basedir, "README.md"), "r") as fh:
   long_description = fh.read()


__version__ = None
with open("wsjsonrpc/_version.py", "r") as fh:
    exec(fh.read()) # redefines __version__


setuptools.setup(
    name='wsjsonrpc',
    version=__version__,
    author="Dónal McMullan",
    author_email="donal.mcmullan@gmail.com",
    description="JSON-RPC 2.0 over websockets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/donalm/wsjsonrpc",
    packages=["wsjsonrpc"],
    install_requires=["autobahn", "twisted"],
    classifiers=[
        "Topic :: Communications",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Framework :: Twisted",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords=["websocket", "twisted", "autobahn", "jsonrpc", "rpc"],
    zip_safe=False,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
)
