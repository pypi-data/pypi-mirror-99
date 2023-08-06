#!/usr/bin/env python3
"""Set up the Python API client for Glances."""
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="glances_api",
    version="0.2.1",
    description="Python API for interacting with Glances.",
    long_description=long_description,
    url="https://github.com/home-assistant-ecosystem/python-glances-api",
    download_url="https://github.com/home-assistant-ecosystem/python-glances-api/releases",
    author="Fabian Affolter",
    author_email="fabian@affolter-engineering.ch",
    license="MIT",
    install_requires=["aiohttp>=3.7.4,<4", "async_timeout<4"],
    packages=["glances_api"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
)
