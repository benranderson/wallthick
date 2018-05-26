#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import wallthick

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    # TODO: Put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(benranderson): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: Put package test requirements here
]

setup(
    name='wallthick',
    version=wallthick.__version__,
    description='PD8010 wall thickness calculations',
    long_description=readme,
    author='Ben Randerson',
    author_email='ben.m.randerson@gmail.com',
    url='https://github.com/benranderson/wallthick',
    packages=find_packages(include=['wallthick']),
    entry_points={
        'console_scripts': [
            'wallthick=wallthick.cli:main',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license='MIT License',
    zip_safe=False,
    keywords='wall thickness engineering pipelines',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
