#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import cliquery


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cliquery',
    version=cliquery.__version__,
    description='a command-line browser interface',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
    keywords='cliquery command line console help answer google bing search feeling lucky wolfram alpha knowledge engine scientific computation internet browser interface bookmark pyteaser preview',
    author='Hunter Hammond',
    author_email='huntrar@gmail.com',
    maintainer='Hunter Hammond',
    maintainer_email='huntrar@gmail.com',
    url='https://github.com/huntrar/cliquery',
    license='MIT',
    packages=find_packages(),
    package_data={'cliquery': ['.cliqrc']},
    entry_points={
        'console_scripts': [
            'cliquery = cliquery.cliquery:command_line_runner',
        ]
    },
    install_requires=[
        'lxml',
        'requests',
        'requests-cache',
        'six'
    ],
)
