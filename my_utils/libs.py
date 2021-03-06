# -*- coding: utf-8 -*-
import base64
import os
import random
import string

from .logger import line_logger

__all__ = [
    'random_password', 'get_dir_path', 'header_to_dict', 'cookie_to_dict',
    'form_encode', 'form_decode', 'base64_decode'
]

logger = line_logger(__name__)


def base64_decode(base64_str):
    """base64长度自动补全并解码"""
    need_padding = len(base64_str) % 4
    if need_padding:
        missing_padding = 4 - need_padding
        base64_str += '=' * missing_padding

    return base64.urlsafe_b64decode(base64_str).decode('utf-8')


def random_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([random.choice(chars) for _ in range(length)])


def get_dir_path(file_dir_path, dirname='.'):
    """获取目录路径，如果目录不存在则报错

    >>> get_dir_path(__file__, '.')     # cur_dir
    '/Users/wanli/Documents/my_py_tools'
    >>> get_dir_path(__file__, '..')    # parent_dir
    '/Users/wanli/Documents'
    >>> get_dir_path(/data/temp, '..')  # /data/temp is no exists
    raise err
    """
    if os.path.isfile(file_dir_path):
        file_dir_path = os.path.dirname(os.path.abspath(file_dir_path))

    dir_path = os.path.abspath(os.path.join(file_dir_path, dirname))
    if os.path.exists(dir_path):
        return dir_path
    else:
        raise Exception('"{}" is no exists'.format(dir_path))


def header_to_dict(values, default=None):
    """HTTP字符串headers转字典

    >>> HEADERS = '''
            Host: easy.lagou.com
            Connection: keep-alive
            X-Anit-Forge-Token:
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
        '''
    >>> header_to_dict(HEADERS)
    {'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
     'Connection': 'keep-alive',
     'Host': 'easy.lagou.com',
     'X-Anit-Forge-Token': ''}
    """
    if not isinstance(values, str):
        return default
    headers = {}
    for i in values.split('\n'):
        if i.strip():
            kv = i.split(':', 1)
            headers.update({kv[0].strip(): kv[-1].strip()})
    return headers


def cookie_to_dict(values, default=None):
    """HTTP字符串cookies转字典

    >>> cookies = 'a=111111111;b=222'
    >>> cookie_to_dict(cookies)
    {'a': '111111111', 'b': '222'}
    """
    if not isinstance(values, str):
        return default
    cookies = {}
    for i in values.split(';'):
        if i.strip():
            kv = i.split('=', 1)
            if '|' in kv[-1]:
                cookies.update({kv[0].strip(): {j.split('=', 1)[0].strip(): j.split('=', 1)[-1].strip() for j in
                                                kv[-1].split('|')}})
            else:
                cookies.update({kv[0].strip(): kv[-1].strip()})
    return cookies


def form_encode(values, sort=True):
    """dict转用&拼接的参数

    >>> data = {'name': 'miles', 'age': 1}
    >>> form_encode(data)
    'name=miles&age=1'
    """
    if not isinstance(values, dict):
        return None
    try:
        keys = values.keys()
        if sort:
            keys = sorted(keys)
    except Exception as e:
        logger.warning('{}: {}'.format(values, e))
    else:
        result = '&'.join('{}={}'.format(k, values[k]) for k in keys)
        return result


def form_decode(values, default=None):
    """用&拼接的参数转换成dict

    >>> data = 'name=miles&age=1'
    >>> form_decode(data)
    data = {'name': 'miles', 'age': 1}
    """
    if not isinstance(values, str):
        return default

    try:
        result = {item.split('=')[0]: item.split('=')[1] for item in values.split('&') if item}
    except Exception as e:
        logger.warning(e)
    else:
        return result
