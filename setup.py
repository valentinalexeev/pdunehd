#!/usr/bin/env python

from distutils.core import setup

setup(name='pdunehd',
	version='1.2',
	description='A Python wrapper for Dune HD media player API',
	author='Valentin Alexeev',
	author_email='valentin.alekseev@gmail.com',
	url='https://github.com/valentinalexeev/pdunehd',
	packages=['pdunehd'],
	install_requires=['requests']
)