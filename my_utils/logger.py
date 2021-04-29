#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging


__all__ = [
    'color_logger', 'line_logger', 'json_logger', 'logger'
]

DATEFMT = '%Y-%m-%d %H:%M:%S'


class ColoredStreamHandler(logging.StreamHandler):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = ['\033[0;{}m'.format(i) for i in range(30, 38)]
    RESET = '\033[0m'

    def format(self, record):

        levelno = record.levelno
        if levelno == 10:
            message = '%(message)s'
        elif levelno == 20:
            message = '{}%(message)s{}'.format(self.GREEN, self.RESET)
        elif levelno == 30:
            message = '{}%(message)s{}'.format(self.YELLOW, self.RESET)
        else:
            message = '{}%(message)s{}'.format(self.RED, self.RESET)

        fmt = '%(asctime)s [%(levelname).1s] [%(filename)s %(funcName)s %(lineno)d] |{} {}'.format(
            self.RESET, message
        )
        fmter = logging.Formatter(fmt=fmt, datefmt=DATEFMT)
        return fmter.format(record)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


def color_logger(name='color_logger', level=logging.DEBUG):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    sh = ColoredStreamHandler()
    sh.setLevel(level)

    sh_fp = f'{sh.name}_{sh.level}'
    handler_seen = {f'{h.name}_{h.level}' for h in log.handlers}
    if sh_fp not in handler_seen:
        log.addHandler(sh)

    return log


def line_logger(name='line_logger', level=logging.DEBUG, handler=logging.StreamHandler()):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # if not log.hasHandlers():
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname).1s] [%(filename)s %(funcName)s %(lineno)d] | %(message)s',
        datefmt=DATEFMT,
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)

    sh_fp = f'{handler.name}_{handler.level}_{handler.formatter._fmt}'
    handler_seen = {f'{h.name}_{h.level}_{h.formatter._fmt}' for h in log.handlers}
    if sh_fp not in handler_seen:
        log.addHandler(handler)

    return log


def json_logger(name='json_logger', level=logging.DEBUG, handler=logging.StreamHandler()):
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
    handler.setLevel(level)
    handler.setFormatter(formatter)

    sh_fp = f'{handler.name}_{handler.level}_{handler.formatter._fmt}'
    handler_seen = {f'{h.name}_{h.level}_{h.formatter._fmt}' for h in log.handlers}
    if sh_fp not in handler_seen:
        log.addHandler(handler)

    return log


logger = line_logger(__name__)
