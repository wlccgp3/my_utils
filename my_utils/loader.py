# -*- coding: utf-8 -*-
from jmespath import search, compile
from parsel.selector import Selector, SelectorList
from parsel.utils import flatten, extract_regex
from .tools import MagicList, MagicDict, MagicStr, TakeFirst, Identity
from .logger import SHlogger

__all__ = ['ItemLoader', 'JmesLoader', 'ComposeLoader']

logger = SHlogger(__name__).logger


class CustomSelectorList(SelectorList):
    @staticmethod
    def _save_mode(values):
        if isinstance(values, str):
            return MagicStr(values)
        elif isinstance(values, list):
            return MagicList(values)
        else:
            return values

    def _get_value(self, values, *processors, op=None):
        values = self._save_mode(values)
        for proc in processors:
            if values is None:
                break
            try:
                values = flatten(proc(value) for value in values if value)
            except Exception as e:
                break
        values = op(values)
        return self._save_mode(values)

    def proc(self, *processors, op=TakeFirst()):
        op = Identity() if op is None else op
        return self._get_value(self.getall(), *processors, op=op)


class ItemLoader(Selector):
    """
    >>> r = requests.get(url)
    >>> loader = ItemLoader(text=r.text)
    >>> tr_list = loader.css('.standard-table tbody tr')
    >>> for tr in tr_list:
            print(tr.xpath('./td[1]//text()').proc(ReFind(r'\S+')))  # default op=TakeFirst()
            print(tr.xpath('./td[2]//text()').proc(ReFind(r'\S+'), op=Join()))
            print(tr.xpath('./td[3]//text()').proc(lambda x: x.split('/')), op=None)
            print(tr.xpath('./td[4]//text()').getall()
    """
    selectorlist_cls = CustomSelectorList

    @staticmethod
    def _save_mode(values):
        if isinstance(values, str):
            return MagicStr(values)
        elif isinstance(values, list):
            return MagicList(values)
        else:
            return values

    def _get_value(self, values, *processors, op=None):
        values = self._save_mode(values)
        for proc in processors:
            if values is None:
                break
            try:
                values = proc(values)
            except Exception as e:
                break
        values = op(values)
        return self._save_mode(values)

    def proc(self, *processors, op=TakeFirst()):
        op = Identity() if op is None else op
        return self._get_value(self.getall(), *processors, op=op)


class JmesList(list):
    def __getitem__(self, pos):
        o = super().__getitem__(pos)
        return self.__class__(o) if isinstance(pos, slice) else o

    @staticmethod
    def _save_mode(values):
        if isinstance(values, str):
            return MagicStr(values)
        elif isinstance(values, list):
            return MagicList(values)
        else:
            return values

    def node(self, values):
        return self.__class__(flatten(flatten([x.node(values) for x in self])))

    def _get_value(self, values, *processors, op=None):
        values = self._save_mode(values)
        for proc in processors:
            if values is None:
                break
            try:
                values = flatten(proc(value) for value in values if value)
            except Exception as e:
                break
        values = op(values)
        return self._save_mode(values)

    def getall(self):
        return [x.getall() for x in self]

    def proc(self, *processors, op=TakeFirst()):
        op = Identity() if op is None else op
        return self._get_value(self.getall(), *processors, op=op)


class JmesLoader(object):
    """base on jmespath, http://jmespath.org/tutorial.html

    列表中有字符串一定要用单引号，比如：
        JmesLoader(result).node("data[?object.question.type=='question']").getall()

    >>> src_data = {
            "people": [
                {"first": "James", "last": "d"},
                {"missing": "1111"},
                {"first": "Jacob", "last": "e"},
                {"first": "Jayden", "last": "f"},
                {"missing": "different"}
            ],
            "foo": {"bar": "baz"},
            'bar': 1,
        }
    >>> loader = JmesLoader(src_data)
    >>> loader.node('people[?keys(@)[?starts_with(@, `first`)]]')
    >>> for item in loader.node('people[?keys(@)[?starts_with(@, `first`)]]'):
            b = item.node('first').proc(lambda x: x.upper(), op=None)
            c = item.node('firsts').proc(lambda x: x.upper())         # default op=TakeFirst()
            d = item.node('last').proc()
            e = item.node('last').getall()
            print(a, b, c, d, e)
    ['JAMES'] None d ['d']
    ['JACOB'] None e ['e']
    ['JAYDEN'] None f ['f']

    >>> print(loader.node('people[][first, missing][]').proc(op=Join(' ')))
    James 1111 Jacob Jayden different
    """
    jme_cls = JmesList

    def __init__(self, src_data, _expr=None):
        self.src_data = src_data
        self._expr = _expr

    def _get_node(self, node):
        expr = compile(node)
        result = expr.search(self.src_data)
        return result

    def getall(self):
        return self.src_data

    def node(self, query):
        values = self._get_node(query)
        if values is None:
            values = []
        elif isinstance(values, (list, tuple)):
            pass
        else:
            values = [values]

        values = [self.__class__(v, query) for v in values]
        return self.jme_cls(values)

    def __bool__(self):
        return bool(self.getall())
    __nonzero__ = __bool__

    def __str__(self):
        data = repr(self.getall())
        return "<%s node=%r data=%s>" % (type(self).__name__, self._expr, data)
    __repr__ = __str__


class ComposeLoader(object):
    def __init__(self, src_data):
        if src_data is None:
            self.src_data = []
        elif isinstance(src_data, (list, tuple)):
            self.src_data = src_data
        else:
            self.src_data = [src_data]

    @staticmethod
    def _save_mode(values):
        if isinstance(values, str):
            return MagicStr(values)
        elif isinstance(values, list):
            return MagicList(values)
        else:
            return values

    def _get_value(self, values, *processors, op=None):
        values = self._save_mode(values)
        for proc in processors:
            if values is None:
                break
            try:
                values = flatten(proc(value) for value in values if value)
            except Exception as e:
                break
        values = op(values)
        return self._save_mode(values)

    def proc(self, *processors, op=TakeFirst()):
        op = Identity() if op is None else op
        return self._get_value(self.src_data, *processors, op=op)
