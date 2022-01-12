#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    with open(filename) as f:
        return f.read()


def find_version():
    version_file = read("flake8_kw_only_args.py")
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


readme = read("README.md")

requirements = [
    "flake8",
    "attrs",
]

test_requirements = [
    "tox",
    "ddt",
]

setup(
    name="flake8_kw_only_args",
    version=find_version(),
    description="Enforce use of kw-only instead of default kw args.",
    long_description_content_type='text/markdown',
    long_description=\
        "Positional parameters can unintentionally set default kwargs: "
        "`def default(key=value)`; instead use kw-only args: "
        "`def kw_only(*, key=value)`.",
    author="Andrew Gaul",
    author_email="gaul@gaul.org",
    url="https://github.com/gaul/flake8_kw_only_args",
    py_modules=[
        "flake8_kw_only_args",
    ],
    include_package_data=True,
    python_requires=">=3.0",
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords="flake8_kw_only_args",
    classifiers=[
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    test_suite="tests",
    tests_require=requirements + test_requirements,
    entry_points={
        "flake8.extension": [
            "K80 = flake8_kw_only_args:KwOnlyArgsChecker",
        ],
    }
)
