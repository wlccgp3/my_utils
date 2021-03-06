# -*- coding: utf-8 -*-
# 该模块主要用于loader做处理函数，也可以单独使用

import re
from datetime import datetime

import arrow

from .mapping import BAIJIAXING

__all__ = [
    'MagicBase', 'MagicList', 'MagicStr', 'TakeFirst', 'Identity', 'Strip', 'Split', 'ReSplit',
    'ReFind', 'ReSub', 'Join', 'ToInt', 'ToAge', 'HighestDegree', 'DateToBack', 'CheckName', 'CheckSurname',
    'FormatTime', 'TakeByIndex', 'ToFloat', 'TakeAllTrue',
]


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

    def __str__(self, *args, **kwargs):
        return super(MagicStr, self).__str__(*args, **kwargs)

    def __getitem__(self, item):
        return MagicBase(str.__getitem__)(self, item)


# 以下对列表操作
class TakeByIndex(object):
    """获取可迭代对象的一个元素，默认取第一个，默认返回None"""

    def __init__(self, index=0, default=None):
        self.index = index
        self.default = default

    def __call__(self, values):
        try:
            return values[self.index]
        except Exception:
            return self.default


class TakeFirst(object):
    """获取可迭代对象的第一个不为空元素"""

    def __init__(self, default=None):
        self.default = default

    def __call__(self, values):
        if values:
            for value in values:
                if value is not None and value != '':
                    return value
        else:
            return self.default


class TakeAllTrue(object):
    """获取子元素bool为True的列表"""

    def __init__(self, default=None):
        if default is None:
            default = []
        self.default = default

    def __call__(self, values):
        if values:
            return [value for value in values if value]
        else:
            return self.default


class Identity(object):
    """对输入不处理"""

    def __call__(self, values):
        return values


# 以下对列表子元素操作
class Strip(object):
    def __init__(self, chars=None):
        self.chars = chars

    def __call__(self, value: str):
        if isinstance(value, str):
            return value.strip(self.chars)
        else:
            return value


class Split(object):
    def __init__(self, sep, maxsplit=-1):
        self.sep = sep
        self.maxsplit = maxsplit

    def __call__(self, value: str):
        if isinstance(value, str):
            return MagicList(value.split(sep=self.sep, maxsplit=self.maxsplit))
        else:
            return MagicList()


class ReSplit(object):
    def __init__(self, pattern, maxsplit=0, flags=0):
        self.pattern = pattern
        self.maxsplit = maxsplit
        self.flags = flags

    def __call__(self, value: str):
        if isinstance(value, str):
            return MagicList(re.split(self.pattern, value, self.maxsplit, self.flags))
        else:
            return value


class ReFind(object):
    def __init__(self, pattern, flags=re.S):
        self.pattern = pattern
        self.flags = flags

    def __call__(self, value: str):
        if isinstance(value, str):
            return MagicList(re.findall(self.pattern, value, self.flags))
        else:
            return MagicList()


class ReSub(object):
    def __init__(self, pattern, repl, count=0, flags=re.S):
        self.pattern = pattern
        self.repl = repl
        self.count = count
        self.flags = flags

    def __call__(self, value: str):
        if isinstance(value, str):
            return MagicStr(re.sub(self.pattern, self.repl, value, self.count, self.flags))
        else:
            return MagicStr()


class Join(object):
    def __init__(self, separator=u''):
        self.separator = separator

    def __call__(self, values):
        if isinstance(values, (list, tuple)):
            values = [value for value in values if value]
        return MagicBase(self.separator.join)(values)


class ToFloat(object):
    def __init__(self, default=None):
        self.default = default

    def __call__(self, value: [str, int, float]):
        try:
            if isinstance(value, str):
                result = float(value.strip().replace(',', ''))
            else:
                result = float(value)
        except Exception as e:
            return self.default
        else:
            return result


class ToInt(object):
    def __init__(self, default=None):
        self.default = default

    def __call__(self, value: [str, int, float]):
        try:
            result = int(ToFloat()(value))
        except Exception as e:
            return self.default
        else:
            return result


class ToAge(object):
    """出生日期转年龄"""

    def __call__(self, value):
        if isinstance(value, str):
            date = FormatTime()(value)
        elif isinstance(value, datetime):
            date = value
        else:
            date = None

        if date:
            return datetime.now().year - date.year
        else:
            return None


class HighestDegree(object):
    """找出最高学历"""

    def __call__(self, value):
        degree_mapping = {
            5: '博士',
            4: '硕士',
            3: '本科',
            2: '大专',
        }
        seen = set()
        for k, v in degree_mapping.items():
            match = ReFind(v)(value)[0]
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

    def __call__(self, value):
        if not isinstance(value, str):
            return self.default
        if '先生' in value or '女士' in value or len(value) < 2:
            return self.default
        if MagicStr(value)[0] not in BAIJIAXING.keys():
            return self.default
        return value


class CheckSurname(object):
    """检测姓氏的有效性"""

    def __init__(self, default=None):
        self.default = default

    def __call__(self, value):
        if not isinstance(value, str):
            return self.default
        surname = MagicStr(value)[0]
        if surname in BAIJIAXING.keys():
            return surname


class FormatTime(object):
    """格式化时间格式"""

    def __init__(self, pattern=None):

        patterns = [
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D]m[\D]s[\D]a[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D]m[\D]s[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D]m[\D]a[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D]m[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D]a[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D+]H[\D*]',
            r'[\D*]YYYY[\D]M[\D]D[\D*]',
            r'[\D*]YYYY[\D]M[\D*]',
            r'[\D*]YYYY[\D*]',
        ]
        self.patterns = []
        for pat in patterns:
            self.patterns.extend([pat, pat[2:]])

        if pattern:
            self.patterns.insert(0, pattern)

    def __call__(self, value):
        try:
            value = arrow.get(value, self.patterns)
        except Exception as e:
            try:
                return arrow.get(value).to('local').datetime
            except Exception as e:
                return None
        else:
            return value.datetime
