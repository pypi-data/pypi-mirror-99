#!/usr/bin/env python
# -*- coding:utf-8 -*-
# leiyh

from setuptools import setup

setup(
    name = "leiyh-api",  # 这里是pip项目发布的名称
    version = "0.0.1",  # 版本号，数值大的会优先被pip
    keywords = ["init", "leiyh-api-test"],  # 被搜索的关键字
    description = "雷阳洪API依赖包",  # 概要描述
    long_description = "雷阳洪API自动化依赖包和脚手架脚本",
    license="MIT Licence",
    url="https://gitee.com/lei-yanghong/leiyh-api-test.git",author="leiyh",
    author_email="leiyh0802@126.com",
    # packages=['tools'],
    # data_files =['init_tool.py'],
    install_requires=[
        # 'Faker==6.5.0', # 随机生成仿真数据
        # 'pinyin==0.4.0',  # 中文转拼音
        'PyMySQL==0.9.3',  # mysql数据库操作
        'xlrd==1.2.0',  # excel读取
        'xlwt==1.3.0',  # excel写入
        'pyyaml==5.1.2',  # yaml文件操作
        'allure-pytest==2.7.0',  # 测试报告框架
        'pytest==5.0.1',  # 单元测试框架
        'pytest-ordering==0.6',  # pytest用例排序
        'requests==2.22.0',  # http接口测试框架
        'python-dateutil==2.8.0',  # 时间工具
        'zipp==3.4.0'
    ]
)

