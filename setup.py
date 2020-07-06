#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdunehd",
    version="1.3.2",
    author="Valentin Alexeev",
    author_email="valentin.alekseev@gmail.com",
    description="A Python wrapper for Dune HD media player API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/valentinalexeev/pdunehd',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
