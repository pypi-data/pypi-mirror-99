# This Python file uses the following encoding:gbk

from setuptools import setup, find_packages
with open('README.txt', 'r',encoding='utf-8') as f:
    README = f.read()
    pass
setup(
name='geo-com-cal',
version='0.0.0',
description='基于python3.5+pyside2-5.15.1实现的大地测量综合计算',
long_description =README,
author='pby',
author_email='2567469480@qq.com',
url='https://github.com',
py_modules=['Geo','images','RollLabel','Task','UI'],
license="LGPL",
platforms=["any"],
packages=find_packages(),
include_package_data=True,
python_requires='>=2.7',

# install_requires 在安装模块时会自动安装依赖包
install_requires=[
'PySide2>=5.11.0,<=6.0.0'
],
)
