# -*- coding: utf-8 -*-
from peewee import MySQLDatabase, SENTINEL

from .decorator import timer


class TimerMySQLDatabase(MySQLDatabase):
    """
    打印sql执行时间
    see: https://github.com/coleifer/peewee/issues/2370
    """

    @timer
    def execute_sql(self, sql, params=None, commit=SENTINEL):
        return super().execute_sql(sql, params, commit)
