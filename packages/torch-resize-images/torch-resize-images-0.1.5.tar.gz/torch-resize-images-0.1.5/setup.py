#!/usr/bin/env python
import os
from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='torch-resize-images',
    version='0.1.5',
    description='A Python library to resize images using PyTorch',
    url='https://github.com/NilsHendrikLukas/torch-resize-images',
    author='Nils Lukas',
    author_email='nlukas@uwaterloo.ca',
    scripts=["./torch_resize"],
    license='MIT',
    keywords='resize image pytorch',
    packages=find_packages(),
    install_requires=['Pillow>=5.1.0', 'torch', 'torchvision', 'gputil', 'tqdm']
)