#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='getmysql2clickhouse',
    version="0.5",
    author='Zhihao Gong',
    author_email='zhihaogong25@gmail.com',
    license='MIT License',
    packages=['getmysql2clickhouse'],
    platforms=["all"],
    url='https://github.com/zhihaogong25/getmysql2clickhouse',
    install_requires=["clickhouse-driver==0.2.0","pymysql==1.0.2","psutil==5.7.2"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
