#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from pathlib import Path

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("docs/about/history.md") as history_file:
    history = history_file.read()


def strip_comments(l):
    return l.split("#", 1)[0].strip()


def _pip_requirement(req, *root):
    if req.startswith("-r "):
        _, path = req.split()
        return reqs(*root, *path.split("/"))
    return [req]


def _reqs(*f):
    path = (Path.cwd() / "reqs").joinpath(*f)
    with path.open() as fh:
        reqs = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r, *f[:-1]) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


install_requires = reqs("base.txt")
test_requires = reqs("test.txt") + install_requires

setup(
    author="Carlo Mazzaferro",
    author_email="carlo.mazzaferro@taktile.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Taktile's Profiling Module ",
    include_package_data=True,
    keywords="taktile-profiling",
    name="taktile-profiling",
    setup_requires=install_requires,
    install_requires=install_requires,
    test_suite="tests",
    packages=find_packages(),
    tests_require=test_requires,
    url="https://github.com/taktile-org/taktile-profiling",
    version="0.3.6",
    zip_safe=False,
)
