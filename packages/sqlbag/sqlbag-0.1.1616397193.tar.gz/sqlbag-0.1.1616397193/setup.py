#!/usr/bin/env python

import io

from setuptools import find_packages, setup

with io.open("README.rst") as f:
    readme = f.read()

setup(
    name="sqlbag",
    version="0.1.1616397193",
    url="https://github.com/djrobstep/sqlbag",
    description="various snippets of SQL-related boilerplate",
    long_description=readme,
    author="Robert Lechte",
    author_email="robertlechte@gmail.com",
    install_requires=[
        "pathlib; python_version<'3'",
        "six",
        "sqlalchemy"],
    zip_safe=False,
    packages=find_packages(),
    classifiers=["Development Status :: 3 - Alpha"],
    extras_require={
        "pg": ["psycopg2"],
        "pendulum": ["pendulum", "relativedelta"],
        "maria": ["pymysql"],
    },
)
