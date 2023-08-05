"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='nhm_spider',
    version='1.22',
    author='noHairMan',
    author_email='zongxuheng@163.com',
    url="https://github.com/noHairMan/nhm-spider",
    description='base on asyncio, spider module like scrapy.',
    long_description=long_description,  # 这里是文档内容, 读取readme文件
    long_description_content_type='text/markdown',  # 文档格式
    packages=find_packages(),
    classifiers=[  # 这里我们指定证书, python版本和系统类型
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # 这里指定python版本号必须大于3.6才可以安装
    install_requires=["aiomysql", "scrapy", "aiohttp"]  # 我们的模块所用到的依赖, 这里指定的话, 用户安装你的模块时, 会自动安装这些依赖
)
