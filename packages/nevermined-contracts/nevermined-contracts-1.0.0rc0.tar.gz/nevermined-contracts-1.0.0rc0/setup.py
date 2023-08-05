#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup
import os
from glob import glob


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []


test_requirements = []
artifact_folder = 'artifacts'
print("Adding all files in /{}".format(artifact_folder))
data_files = [(artifact_folder, [f for f in glob(os.path.join(artifact_folder, '*'))])]

print("data_files=")
for df in data_files:
    print(df)

setup(
    author="nevermined-io",
    author_email='root@nevermined.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Smart Contracts for Nevermined Data platform",
    data_files=data_files,
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='nevermined-contracts',
    name='nevermined-contracts',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nevermined-io/contracts',
    version='1.0.0-rc0',
    zip_safe=False,
)
