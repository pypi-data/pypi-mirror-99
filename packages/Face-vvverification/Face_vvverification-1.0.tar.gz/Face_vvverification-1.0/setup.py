from setuptools import setup, find_packages


setup(
    name='Face_vvverification',# 本模块要发布的名字
    version='v1.0',#版本
    description='A  module for face verification', # 简要描述
    py_modules=find_packages(),   #  需要打包的模块
    author='Show_me_your_code', # 作者名
    author_email='gavinxuai@gmail.com',   # 作者邮件
    url='', # 项目地址,一般是代码托管的网站
    # requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
    license='MIT'
)