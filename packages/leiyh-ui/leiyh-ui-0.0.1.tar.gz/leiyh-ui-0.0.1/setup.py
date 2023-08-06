#!/usr/bin/env python
# -*- coding:utf-8 -*-
# leiyh
from setuptools import setup

setup(
    name="leiyh-ui",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=["init", "auto-ui-test"],  # 被搜索的关键字
    description="雷阳洪UI依赖包",  # 概要描述
    long_description="雷阳洪UI自动化依赖包和脚手架脚本",  # 详细描述
    # license，软件授权许可 。
    # MIT许可证（The MIT License）是许多软件授权条款中，被广泛使用的其中一种。
    # 与其他常见的软件授权条款（如GPL、LGPL、BSD）相比，MIT是相对宽松的软件授权条款。
    license="MIT Licence",
    url="https://gitee.com/lei-yanghong/leiyh-ui-test.git",  # 项目相关文件地址，一般是github
    author="leiyh",  # 作者
    author_email="leiyh0802@126.com",  # 邮箱
    # packages=['tools'],
    # data_files =['init_tool.py'],
    install_requires=[
        # 'Faker==6.5.0', # 随机生成仿真数据
        # 'pinyin==0.4.0',  # 中文转拼音
        "allure-pytest==2.7.0"
        "allure-python-commons==2.7.0"
        "atomicwrites==1.4.0"
        "attrs==20.2.0"
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "colorama==0.4.4"
        "gy-ui-tools==1.0.5"
        "idna==2.10"
        "importlib-metadata==2.0.0"
        "more-itertools==8.5.0"
        "packaging==20.4"
        "pinyin==0.4.0"
        "pluggy==0.13.1"
        "py==1.9.0"
        "pyautoit-win64==1.0.3"
        "PyMySQL==0.9.3"
        "pyparsing==2.4.7"
        "pytest==5.0.1"
        "pytest-ordering==0.6"
        "PyYAML==5.1.2"
        "requests==2.25.0"
        "selenium==3.141.0"
        "six==1.15.0"
        "urllib3==1.25.11"
        "wcwidth==0.2.5"
        "xlrd==1.2.0"
        "xlwt==1.3.0"
        "zipp==0.6.0"
    ]
)