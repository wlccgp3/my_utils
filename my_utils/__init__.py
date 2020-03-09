#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from .useragent import random_ua
from .mongoclient import Mongo
from .loader import *
from .libs import *
from .temp import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s [%(name)s %(lineno)d] %(levelname)s | %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
