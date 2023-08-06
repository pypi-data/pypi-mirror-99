# -*- coding: utf-8 -*-
import time
from functools import wraps
from typing import Iterable

from .model import DictModel
from .logger import logger


def to_dict(func):
    """
    model to dict , shallow convert
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        logger.debug('decorator: to dict')

        result = func(*args, **kwargs)

        def _to_dict(item):
            if isinstance(item, DictModel):
                return item.to_dict()
            else:
                return item

        if isinstance(result, Iterable):
            return list(map(_to_dict, result))
        else:
            return _to_dict(result)

    return decorator


# 返回嵌套字典
def to_data(func=None, recurse=True, backrefs=False,
            only=None, exclude=None,
            seen=None, extra_attrs=None,
            fields_from_query=None, max_depth=1,
            manytomany=False):
    """model to dict , deep convert"""

    def inner(inner_func):
        @wraps(inner_func)
        def decorator(*func_args, **func_kwargs):
            logger.debug('decorator: to data')

            result = inner_func(*func_args, **func_kwargs)

            def _to_data(item):
                if isinstance(item, DictModel):
                    return item.to_data(
                        recurse=recurse, backrefs=backrefs,
                        only=only, exclude=exclude,
                        seen=seen, extra_attrs=extra_attrs,
                        fields_from_query=fields_from_query,
                        max_depth=max_depth, manytomany=manytomany)
                else:
                    return item

            if isinstance(result, Iterable):
                return list(map(_to_data, result))
            else:
                return _to_data(result)

        return decorator

    if func is None:
        return inner
    else:
        return inner(func)


def timer(func):
    """计时器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        ret = func(*args, **kwargs)

        end_time = time.time()
        logger.debug("time: %.2f s" % (end_time - start_time))

        return ret

    return wrapper
