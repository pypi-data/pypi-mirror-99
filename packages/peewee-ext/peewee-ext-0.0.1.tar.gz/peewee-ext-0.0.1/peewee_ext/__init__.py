# -*- coding: utf-8 -*-


from playhouse.db_url import schemes, register_database, connect as peewee_connect

from .database import TimerMySQLDatabase
from .model import DictModel
from .decorator import to_dict, to_data, timer

register_database(TimerMySQLDatabase, 'mysql+timer')


def connect(db_url=None, **kwargs):
    if db_url:
        return peewee_connect(db_url, **kwargs)
    else:
        scheme = kwargs.pop('scheme')
        return schemes[scheme](**kwargs)
