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

## 使用方式

1、连接方式的增强

```python

db_config = {
    'scheme': 'mysql',    # 增加数据库类型
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'data'
}

# 用peewee_ext.connect 替换peewee的connect
# from playhouse.db_url import connect
from peewee_ext import connect


# 可以传入关键字参数，当然第一个位置参数也支持url地址链接
db = connect(**db_config)
```

2、打印sql执行时间

```python

# from peewee import MySQLDatabase 
from peewee_ext import TimerMySQLDatabase


db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'data'
}

# 打印sql执行时间
# db = MySQLDatabase(**db_config)
db = TimerMySQLDatabase(**db_config)

# 对应connect参数 ：
# 'scheme': 'mysql+timer'
```

3、Model转dict字典对象

```python

from peewee_ext import DictModel, to_dict, to_data

# 用 DictModel 替换 Model
# class BaseModel(Model): 
class BaseModel(DictModel):
    class Meta:
        database = db

```

3.1、Model对象调用方法转dict

```python
model = BaseModel()
model.to_data()
model.to_dict()
```

3.2、使用装饰器转dict

```python
from peewee_ext import to_dict, to_data

# 装饰器将返回值是DictModel对象转换为dict，其他类型原样返回
@to_dict
def get_row():
    """
    可以返回 DictModel 或 List[DictModel]
    """
    return BaseModel.select().first()


# 可选参数参考：playhouse.shortcuts.model_to_dict
@to_data
def get_row():
    """
    可以返回 DictModel 或 List[DictModel]
    """
    return BaseModel.select().first()
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

# 已注册scheme: 'mysql+timer'
class TimerMySQLDatabase(MySQLDatabase):
    """"""

```

