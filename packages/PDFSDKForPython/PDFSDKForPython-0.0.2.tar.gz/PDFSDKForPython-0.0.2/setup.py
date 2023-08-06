#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: ***<***gmail.com>
from setuptools import setup, find_packages
import setuptools
import os
import codecs

# 需要将那些包导入
packages = ["PDFSDKForPython"]

# 导入静态文件
file_data = []
# ("PDFSDKForPython/lib",
#  ["PDFSDKForPython/lib/Windows/FreeImage.dll", "PDFSDKForPython/lib/Windows/FreeImage.dll", "PDFSDKForPython/lib/Windows/license_key.txt", "PDFSDKForPython/lib/Windows/PDFImageProcess.exe"]),
# ]

# 第三方依赖
requires = []

# 自动读取version信息
about = {}
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

with codecs.open(os.path.join(base_path, 'PDFSDKForPython', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

# 自动读取readme
with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=about["__title__"],  # 包名称
    version=about["__version__"],  # 包版本
    description=about["__description__"],  # 包详细描述
    long_description=readme,   # 长描述，通常是readme，打包到PiPy需要
    author=about["__author__"],  # 作者名称
    author_email=about["__author_email__"],  # 作者邮箱
    url=about["__url__"],   # 项目官网
    packages=packages,    # 项目需要的包
    data_files=file_data,   # 打包时需要打包的数据文件，如图片，配置文件等
    include_package_data=True,  # 是否需要导入静态数据文件
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[    # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
