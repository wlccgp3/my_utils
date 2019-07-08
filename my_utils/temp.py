#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import requests
from .logger import SHlogger

logger = SHlogger(__name__).logger

__all__ = ['get_proxy']


def get_proxy(url):
    # url = 'http://127.0.0.1:5000/proxy'
    try:
        result = requests.get(url).json()
    except Exception as e:
        logger.warning(e)
        time.sleep(10)
    else:
        msg = result.get('msg', '')
        if msg == 'success':
            return result['data']

        logger.warning('msg: {}'.format(msg))
