#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from .useragent import random_ua
from .mongoclient import Mongo
from .loader import *
from .libs import *
from .temp import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s %(name)s %(lineno)d] | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# formatter = logging.Formatter(
#     '%(asctime)s [%(levelname)s %(name)s %(lineno)d] | %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.INFO)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)
