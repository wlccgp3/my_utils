# -*- coding: utf-8 -*-
import json
import logging

from rich.logging import RichHandler

__all__ = [
    'line_logger', 'json_logger', 'logger'
]

DATEFMT = '%Y-%m-%d %H:%M:%S'


def line_logger(name='line_logger', level=logging.DEBUG, handler=None):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # if not log.hasHandlers():
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname).1s] [%(filename)s %(funcName)s %(lineno)d] | %(message)s',
        datefmt=DATEFMT,
    )
    handler = handler or logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    sh_fp = f'{handler.name}_{handler.level}_{handler.formatter._fmt}'
    handler_seen = {f'{h.name}_{h.level}_{h.formatter._fmt}' for h in log.handlers}
    if sh_fp not in handler_seen:
        log.addHandler(handler)

    return log


def json_logger(name='json_logger', level=logging.DEBUG, handler=None):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        json.dumps({
            'datetime': '%(asctime)s',
            'level': '%(levelname)s',
            'file': '%(filename)s',
            'function': '%(funcName)s',
            'line': '%(lineno)d',
            'message': '%(message)s',
        }, ensure_ascii=False),
        datefmt=DATEFMT,
    )
    handler = handler or logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    sh_fp = f'{handler.name}_{handler.level}_{handler.formatter._fmt}'
    handler_seen = {f'{h.name}_{h.level}_{h.formatter._fmt}' for h in log.handlers}
    if sh_fp not in handler_seen:
        log.addHandler(handler)

    return log


logger = line_logger(__name__, handler=RichHandler(show_time=False, show_level=False, show_path=False))
