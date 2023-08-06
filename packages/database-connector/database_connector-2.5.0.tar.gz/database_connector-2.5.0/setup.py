#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'cx-Oracle==8.1.0',
    'psycopg2-binary==2.8.6',
    'pymongo==3.11.3',
    'PyMySQL==1.0.2',
    'PyYAML==5.4.1',
]

setup_requirements = []

test_requirements = []

setup(
    author="Adam Gleason",
    author_email='gleasona@email.chop.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Database Connector Class",
    entry_points={
        'console_scripts': [
            'database_connector=database_connector.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='database_connector',
    name='database_connector',
    packages=find_packages(include=['database_connector']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gleasona/database_connector',
    version='2.5.0',
    zip_safe=False,
)
