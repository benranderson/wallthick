# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENCE') as f:
    license = f.read()

setup(
    name='wallthick',
    version='0.0.0',
    description='PD8010 wall thickness calculations',
    long_description=readme,
    url='https://github.com/benranderson/wallthick',
    author='Ben Randerson',
    author_email='ben.m.randerson@gmail.com',
    license=license,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='wall thickness engineering pipelines',
    packages=find_packages(exclude=('tests', 'docs'))
)
