#!/usr/bin/env python
from setuptools import find_namespace_packages, setup
import os
import re
import io
from os import path

setup(
    name='dbt-athena',
    version='0.0.5',
    author="Lucas Saletti",
    author_email="lucas.saletti92@gmail.com",
    description="The athena adapter plugin for dbt (data build tool)",
    url='https://github.com/lsaletti/dbt-athena',
    long_description=io.open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    package_data={
        "dbt": [
            "include/athena/dbt_project.yml",
            "include/athena/sample_profiles.yml",
            "include/athena/macros/*.sql",
            "include/athena/macros/*/*.sql",
        ]
    },
    install_requires=[
#        "dbt-core==0.19.0",
        "pyathena==2.1.1",
    ]
)