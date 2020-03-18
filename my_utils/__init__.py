#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from .useragent import random_ua
from .loader import *
from .libs import *
from .temp import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname).1s] [%(filename)s %(lineno)d] | %(message)s',
)

logger = logging.getLogger(__name__)
