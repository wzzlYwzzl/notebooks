[TOC]

# setuptools

Setuptools是disutils包的增强，让开发者更容易的构建和发布Python包，特别是包与包之间存在相互依赖时。

- 可以创建Python eggs文件。
- 加强了读取压缩包中的数据文件。
- 自动包含代码树中的package，而无需一一列出。
- 无需创建MANIFEST.in文件便可包含所有先关的文件。
- 自动生成封装的脚本或者exe文件。
- 透明支持Cython。

## 1. 基本用法

```python
from setuptools import setup, find_packages
setup(
    name="helloworld",
    version='0.1',
    packages=find_packages(),
    scripts=['say_hello.py'],

    install_requires=['docutils>=0.3'],

    package_data={
        # 表示任何一个package中包含的txt文件、rst文件都会包含到发布的包中。
        '':['*.txt','*.rst'],
        # 表示hello package中的msg文件也会包含到包中。
        'hello':['*.msg']
    }

    # metadata to display on PyPI
    author="Me",
    author_email="me@example.com",
    description="This is an Example Package",
    keywords="hello world example examples",
    url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]

    # could also include long_description, download_url, etc.
)
```

编写完setup.py文件，接下来按照需求执行相应的命令：

- python setup.py --help
- python setup.py build     # 仅编译不安装
- python setup.py install    #安装到python安装目录的lib下
- python setup.py sdist      #生成压缩包(zip/tar.gz)
- python setup.py bdist_wininst  #生成NT平台安装包(.exe)
- python setup.py bdist_rpm #生成rpm包

## 2. 指定项目版本

## 官方文档

1. [setuptools](https://setuptools.readthedocs.io/en/latest/)
