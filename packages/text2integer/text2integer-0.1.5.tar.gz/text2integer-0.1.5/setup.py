#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md") as file:
    read_me_description = file.read()

setup(
  author="Vikash Kumar Prasad",
  author_email='prasad.vikash05@gmail.com',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
  description="Converts text to integers",
  long_description=read_me_description,
  long_description_content_type="text/markdown",
  license="MIT license",
  include_package_data=True,
  name='text2integer',
  version='0.1.5',
  zip_safe=False,
   python_requires='>=3.8',
)

#python setup.py sdist
#twine upload dist/*
