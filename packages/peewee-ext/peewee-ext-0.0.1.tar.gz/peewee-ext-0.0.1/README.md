# Peewee-ext

![PyPI](https://img.shields.io/pypi/v/peewee-ext.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/peewee-ext)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peewee-ext)
![PyPI - License](https://img.shields.io/pypi/l/peewee-ext)

- Github: [https://github.com/mouday/peewee-ext](https://github.com/mouday/peewee-ext)
- Pypi: [https://pypi.org/project/peewee-ext](https://pypi.org/project/peewee-ext)

## 简介

peewee-ext 对 peewee 进行了部分扩展，在其基础上进行了增强

## 安装

```
pip install peewee-ext
```

## 说明 

增加一个 DictModel 增加两个方法

```python
from peewee import Model

class DictModel(Model):

    def to_data(self, recurse=True, backrefs=False,
                only=None, exclude=None,
                seen=None, extra_attrs=None,
                fields_from_query=None, max_depth=None,
                manytomany=False):
        """model to dict"""
  
    def to_dict(self):
        """model to dict"""
        

    def __str__(self):
        """friendly for human"""
        

```

增加两个装饰器

```python
def to_dict(func):
    """
    model to dict , shallow convert
    """

# 返回嵌套字典
def to_data(func=None, recurse=True, backrefs=False,
            only=None, exclude=None,
            seen=None, extra_attrs=None,
            fields_from_query=None, max_depth=1,
            manytomany=False):
    """model to dict , deep convert"""

```

增加执行时间打印

```python
from peewee import MySQLDatabase

class TimerMySQLDatabase(MySQLDatabase):
    """"""

```
