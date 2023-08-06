#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from distutils.command.install import install as _install
from shutil import which

from setuptools import setup


def make_path() -> str:
    path = which("make")
    if not path:
        raise Exception("'make' command not found")
    return path


class install(_install):
    def run(self):
        subprocess.call([make_path(), "clean", "-C", "xcursorgen"])
        subprocess.call([make_path(), "-C", "xcursorgen"])
        _install.run(self)


# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clickgen",
    version="1.1.9",
    author="Kaiz Khatri",
    author_email="kaizmandhu@gmail.com",
    description="The hassle-free cursor building toolbox 🧰",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ful1e5/clickgen",
    cmdclass={"install": install},
    scripts=["scripts/clickgen"],
    project_urls={
        "Source": "https://github.com/ful1e5/clickgen",
        "Funding": "https://www.paypal.me/kaizkhatri",
        "Changelog": "https://github.com/ful1e5/clickgen/blob/main/CHANGELOG.md",
    },
    install_requires=["Pillow>=8.1.1"],
    packages=["clickgen"],
    package_dir={"clickgen": "clickgen"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics",
        "Topic :: System :: Operating System",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    keywords=["cursor", "xcursor", "windows", "linux", "anicursorgen", "xcursorgen"],
    zip_safe=True,
)
