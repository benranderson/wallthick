# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wallthick',
    version='0.0.0',
    description='PD8010 wall thickness calculations',
    long_description=readme,
    author='Ben Randerson',
    author_email='ben.m.randerson@gmail.com',
    url='https://github.com/benranderson/wallthick',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
