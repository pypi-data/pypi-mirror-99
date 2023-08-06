from setuptools import setup
from os.path import join, dirname, abspath

import re

re_ver = re.compile(r"__version__\s+=\s+'(.*)'")
with open(join(abspath(dirname(__file__)), 'mecv', '__init__.py'), encoding='utf-8') as f:
    version = re_ver.search(f.read()).group(1)

import torch

torch_ver = [int(x) for x in torch.__version__.split('.')[:2]]
assert torch_ver >= [1, 1], 'mecv requires PyTorch >= 1.1'

setup(
    name='mecv',
    version=version,
    description='A Modular and Extensible Framework for Computer Vision',
    long_description='See project page: https://github.com/mtli/mecv',
    url='https://github.com/mtli/mecv',
    author='Mengtian (Martin) Li',
    author_email='martinli.work@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='computer vision deep learning pytorch',
    packages=['mecv'],
    python_requires='>=3',
    install_requires=[
        'python-dateutil',
        'py-cpuinfo',
        'numpy',
        'torchvision',
        'tensorboard',
        'linearlr',
    ],
    include_package_data = True,
)
