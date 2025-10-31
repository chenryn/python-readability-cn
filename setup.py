#!/usr/bin/env python

import codecs
import os
import re
import sys
from setuptools import setup, find_packages

# Adapted from https://github.com/pypa/pip/blob/master/setup.py
def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))

    # Intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *file_paths), "r") as fp:
        version_file = fp.read()
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M,
        )
        if version_match:
            return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='readability_cn',
    version=find_version("readability_cn", "__init__.py"),
    author='chenryn',
    author_email='rao.chenlin@gmail.com',
    url="http://github.com/chenryn/python-readability-cn",
    packages=find_packages(),
    description='计算中文文本可读性指标',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'ltp',
        'torch'
    ],
    extras_require={
        'jieba': ['jieba'],
        'pkuseg': ['pkuseg'],
        'all': ['jieba', 'pkuseg']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',
    package_data={
        'readability_cn': [
            'data/*.*'
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'readability_cn=readability_cn.readability:main',
        ],
    },
)
