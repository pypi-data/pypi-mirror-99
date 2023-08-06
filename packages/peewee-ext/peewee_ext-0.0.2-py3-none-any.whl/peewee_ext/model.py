# -*- coding: utf-8 -*-
import datetime
import json

from peewee import Model
from playhouse.shortcuts import model_to_dict


def encode_complex(obj):
    if isinstance(obj, datetime.datetime):
        return obj.__repr__()

    elif isinstance(obj, DictModel):
        return obj.to_dict()


class DictModel(Model):

    def to_data(self, recurse=True, backrefs=False,
                only=None, exclude=None,
                seen=None, extra_attrs=None,
                fields_from_query=None, max_depth=None,
                manytomany=False):
        """model to dict"""
        return model_to_dict(self,
                             recurse=recurse, backrefs=backrefs,
                             only=only, exclude=exclude,
                             seen=seen, extra_attrs=extra_attrs,
                             fields_from_query=fields_from_query,
                             max_depth=max_depth, manytomany=manytomany)

    def to_dict(self):
        """model to dict"""
        return dict(self.__data__)

    def __str__(self):
        """friendly for human"""
        return json.dumps(self, ensure_ascii=False, default=encode_complex)
