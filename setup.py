#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import wallthick

import setuptools


setuptools.setup(
    name='wallthick',
    version=wallthick.__version__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ben Randerson',
    author_email='ben.m.randerson@gmail.com',
    python_requires='>=3.4.0',
    url='https://github.com/benranderson/wallthick',
    packages=setuptools.find_packages(include=['wallthick']),
    entry_points={
        'console_scripts': [
            'wallthick=wallthick.cli:main',
        ],
    },
    install_requires=open('requirements.txt').readlines(),
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
)
