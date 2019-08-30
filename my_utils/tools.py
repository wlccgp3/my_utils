#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 该模块主要用于loader做处理函数，也可以单独使用

import re
import arrow
from datetime import datetime
from .mapping import BAIJIAXING
from .logger import SHlogger

__all__ = [
    'MagicBase', 'MagicList', 'MagicStr', 'MagicDict', 'TakeFirst', 'Identity', 'Strip', 'Split', 'ReSplit',
    'ReFind', 'Join', 'ToInt', 'ToAge', 'HighestDegree', 'DateToBack', 'CheckName', 'CheckSurname',
    'FormatTime',
]

logger = SHlogger(__name__).logger


class MetaClass(type):
    """将Magic类修改成原始类，比如MagicStr -> str
    """
    def __new__(mcs, name, bases, attrs, **kwargs):
        del attrs['__qualname__']
        return type.__new__(mcs, bases[0].__name__, bases, attrs, **kwargs)


class MagicBase(object, metaclass=MetaClass):
    """try except 封装
    """

    def __init__(self, func, default=None):
        self.func = func
        self.default = default

    def __call__(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            return self.default


class MagicList(list, metaclass=MetaClass):
    """基于list封装，取不到元素不报错，返回None

    >>> MagicList([1, 2])[0]
    1
    >>> print(MagicList([1, 2])[2])
    None
    """

    def __getitem__(self, item):
        return MagicBase(list.__getitem__)(self, item)
        # try:
        #     return list.__getitem__(self, item)
        # except Exception as e:
        #     return None

    def get(self, item, default=None):
        result = MagicBase(list.__getitem__)(self, item)
        if result is None:
            result = default
        return result

    def pop(self, index=-1):
        return MagicBase(list.pop)(self, index)


class MagicStr(str, metaclass=MetaClass):
    """基于str封装，取不到元素不报错，返回None

    >>> MagicStr('python')[0]
    'p'
    >>> print(MagicStr('python')[10])
    None
    """

    def __getitem__(self, item):
        return MagicBase(str.__getitem__)(self, item)


class MagicDict(dict, metaclass=MetaClass):
    """基于dict封装，可以点方式获取元素，取不到元素不报错，返回None

    >>> MagicDict({'name': 'miles'}).name
    'miles'
    >>> print(MagicDict({'name': 'miles'}).age)
    None
    """

    # __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        values = dict.get(*args)
        if type(values) is dict:
            return MagicDict(values)
        else:
            return values

    def __getitem__(self, item):
        return MagicBase(dict.__getitem__)(self, item)


class TakeFirst(object):
    """获取可迭代对象的第一个元素"""

    def __init__(self, default=None):
        self.default = default

    def __call__(self, values):
        if values:
            for value in values:
                if value is not None and value != '':
                    return value
        else:
            return self.default


class Identity(object):
    """对输入不处理"""

    def __call__(self, values):
        return values


class Strip(object):
    def __init__(self, chars=None):
        self.chars = chars

    def __call__(self, values):
        if isinstance(values, str):
            return values.strip(self.chars)
        else:
            return values


class Split(object):
    def __init__(self, sep, maxsplit=-1):
        self.sep = sep
        self.maxsplit = maxsplit

    def __call__(self, values):
        if isinstance(values, str):
            return MagicList(values.split(sep=self.sep, maxsplit=self.maxsplit))
        else:
            return MagicList()


class ReSplit(object):
    def __init__(self, pattern, maxsplit=0, flags=0):
        self.pattern = pattern
        self.maxsplit = maxsplit
        self.flags = flags

    def __call__(self, values):
        if isinstance(values, str):
            return MagicList(re.split(self.pattern, values, self.maxsplit, self.flags))
        else:
            return values


class ReFind(object):
    def __init__(self, pattern, flags=re.S):
        self.pattern = pattern
        self.flags = flags

    def __call__(self, values):
        if isinstance(values, str):
            return MagicList(re.findall(self.pattern, values, self.flags))
        else:
            return MagicList()


class Join(object):
    def __init__(self, separator=u''):
        self.separator = separator

    def __call__(self, values):
        if isinstance(values, (list, tuple)):
            values = [value for value in values if value]
        return MagicBase(self.separator.join)(values)


class ToInt(object):
    def __init__(self, default=None):
        self.default = default

    def __call__(self, values):
        try:
            result = int(float(values))
        except Exception as e:
            return self.default
        else:
            return result


class ToAge(object):
    """出生日期转年龄"""

    def __call__(self, values):
        if isinstance(values, str):
            date = FormatTime()(values)
        elif isinstance(values, datetime):
            date = values
        else:
            date = None

        if date:
            return datetime.now().year - date.year
        else:
            return None


class HighestDegree(object):
    """找出最高学历"""

    def __call__(self, values):
        degree_mapping = {
            5: '博士',
            4: '硕士',
            3: '本科',
            2: '大专',
        }
        seen = set()
        for k, v in degree_mapping.items():
            match = ReFind(v)(values)[0]
            if match:
                seen.add(k)
        if seen:
            return degree_mapping.get(max(seen))
        else:
            return None


class DateToBack(object):
    """根据已过多少天或小时，计算事件发生的时间"""

    def __call__(self, values):
        if not isinstance(values, str):
            return None

        values = re.sub(r'昨日|昨天', '1天', values)
        values = re.sub(r'前日|前天', '2天', values)
        today = ReFind(r'今日|刚刚|今天|在线')(values)[0]
        re_day = ReFind(r'(\d+?)[天日]')(values)[0]
        re_hour = ReFind(r'(\d+?)小时')(values)[0]
        if today:
            _date = arrow.now().replace(hour=12, minute=0, second=0, microsecond=0).datetime
        elif re_day:
            arw = arrow.now().replace(hour=12, minute=0, second=0, microsecond=0)
            _date = arw.shift(days=-int(re_day)).datetime
        elif re_hour:
            arw = arrow.now().replace(minute=0, second=0, microsecond=0)
            _date = arw.shift(hours=-int(re_hour)).datetime
        else:
            _date = None
        return _date


class CheckName(object):
    """检测姓名的有效性"""

    def __init__(self, default=None):
        self.default = default

    def __call__(self, values):
        if not isinstance(values, str):
            return self.default
        if '先生' in values or '女士' in values or len(values) < 2:
            return self.default
        if MagicStr(values)[0] not in BAIJIAXING.keys():
            return self.default
        return values


class CheckSurname(object):
    """检测姓氏的有效性"""

    def __init__(self, default=None):
        self.default = default

    def __call__(self, values):
        if not isinstance(values, str):
            return self.default
        surname = MagicStr(values)[0]
        if surname in BAIJIAXING.keys():
            return surname


class FormatTime(object):
    """格式化时间格式"""

    def __init__(self, pattern=None):
        self.patterns = [
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}[\D]m{1,2}[\D]s{1,2}[\D]a',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}[\D]m{1,2}[\D]s{1,2}',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}[\D]m{1,2}[\D]a',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}[\D]m{1,2}',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}[\D]a',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}[\D]+H{1,2}',
            r'YY{1,2}[\D]M{1,2}[\D]D{1,2}',
            r'YY{1,2}[\D]M{1,2}',
        ]
        if pattern:
            self.patterns.insert(0, pattern)

    def __call__(self, values):
        try:
            values = arrow.get(values, self.patterns)
        except Exception as e:
            try:
                return arrow.get(values).to('local').datetime
            except Exception as e:
                return None
        else:
            return values.datetime
