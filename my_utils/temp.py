#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import logging
import requests

__all__ = ['get_proxy']

logger = logging.getLogger(__name__)


def get_proxy(url):
    # url = 'http://127.0.0.1:5000/proxy'
    try:
        result = requests.get(url).json()
    except Exception as e:
        logger.warning(e)
        time.sleep(10)
    else:
        msg = result.get('message', '')
        if msg == 'success':
            return result['data']

        logger.warning('msg: {}'.format(msg))
