#!/usr/bin/python
#-*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lycium",
    version="0.0.15",
    author="kevinyjn",
    author_email="kevinyjn@foxmail.com",
    description="Common python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/starview/lycium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pika",
        "redis",
        "gunicorn",
        "mongoengine",
        "elasticsearch",
        "sqlalchemy",
        "Cython",
        "pycrypto",
        "IPy",
        "requests",
        "tornado",
        "zeep",
        "motor",
        "blinker",
        "aredis",
        "sqlalchemy_aio",
        "pyopenssl",
        "rsa",
        "cx_Oracle",
        "pymssql",
        "protobuf",
        "confluent-kafka"
    ]
)
