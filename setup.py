# See license.txt for license details.
# Copyright (c) 2020, Chris Withers

import os

from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

defaults_require = [
    'configurator',
    'orjson',
    'pydantic',
]

test_require = defaults_require + [
    'pytest',
    'pytest-cov',
    'sybil',
    'testfixtures',
]

setup(
    name='mortar',
    version='0.2.0.dev0',
    author='Chris Withers',
    author_email='chris@withers.org',
    license='MIT',
    description=(
        "A dependency injection based web application server framework."
    ),
    long_description=open('README.rst').read(),
    url='https://github.com/mortar/mortar',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'starlette >= 0.13.1',
        'mush >= 3.0.0a1',
    ],
    extras_require=dict(
        defaults=defaults_require,
        test=test_require,
        build=[
            'sphinx',
            'sphinx-rtd-theme',
            'setuptools-git',
            'twine',
            'wheel'
        ]
    ),
)
