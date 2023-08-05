# -*- coding: utf-8 -*-
#
# Copyright 2017 Gehirn Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)
requires = [
    'python-jose[cryptography] ~= 3.0',  # May 4, 2018
    'rfc3986 ~= 1.4',  # Apr 8, 2020
    'WebOb ~= 1.8',  # Apr 5, 2018
]

setup(
    name='ghoauth',
    version='0.7.0',

    description='OAuth Provider Library for Python 3',
    url='https://github.com/GehirnInc/ghoauth',

    author='Kohei YOSHIDA',
    author_email='kohei.yoshida@gehirn.co.jp',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ],

    packages=find_packages(),

    install_requires=requires,
    tests_require=[],
    python_requires='>= 3.6',
)
