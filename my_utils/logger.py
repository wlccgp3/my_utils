#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


__all__ = ['SHlogger']


class ColoredStreamHandler(logging.StreamHandler):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = ['\033[0;{}m'.format(i) for i in range(30, 38)]
    COLOR_CYLE = [GREEN, YELLOW, BLUE, MAGENTA, CYAN]
    RESET = '\033[0m'

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def format(self, record):
        datefmt = '%m-%d %H:%M:%S'
        COLOR = self.COLOR_CYLE[record.process % len(self.COLOR_CYLE)]
        if record.name == 'root':
            name = '%(module)s'
        else:
            name = '%(name)s'

        if record.levelno == 10:
            message = '%(message)s'
        elif record.levelno == 20:
            message = '{}%(message)s{}'.format(self.GREEN, self.RESET)
        else:
            message = '{}%(message)s{}'.format(self.RED, self.RESET)

        FORMAT = '{}%(asctime)s [{} %(funcName)s_%(lineno)d] |{} {}'.format(
            COLOR, name, self.RESET, message
        )
        fmt = logging.Formatter(fmt=FORMAT, datefmt=datefmt)
        return fmt.format(record)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


class SHlogger(object):
    """自定义logger

    >>> logger = SHlogger().logger
    >>> logger = SHlogger(__name__).logger
    """
    def __init__(self, name=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(level)
            self.sh = ColoredStreamHandler()
            self.sh.setLevel(level)
            self.logger.addHandler(self.sh)

