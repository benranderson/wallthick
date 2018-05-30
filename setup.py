#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import wallthick

import setuptools

# Package meta-data.
NAME = 'wallthick'
DESCRIPTION = 'PD8010 wall thickness calculations.'
URL = 'https://github.com/benranderson/wallthick'
EMAIL = 'ben.m.randerson@gmail.com'
AUTHOR = 'Ben Randerson'
REQUIRES_PYTHON = '>=3.4.0'
VERSION = None

# What packages are required for this module to be executed?
requirements = [
    'click',
    'scipy',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

with open('README.md') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name=NAME,
    version=wallthick.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(include=['wallthick']),
    entry_points={
        'console_scripts': [
            'wallthick=wallthick.cli:main',
        ],
    },
    install_requires=requirements,
    setup_requires=setup_requirements,
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    keywords='wall thickness engineering pipelines',
    classifiers=[
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
