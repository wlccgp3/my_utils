#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


__all__ = ['cjy_client']


class ChaojiyingClient(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        try:
            result = requests.post(
                'http://upload.chaojiying.net/Upload/Processing.php',
                data=params, files=files, headers=self.headers
            ).json()
        except Exception as e:
            print(e)
        else:
            return result

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


cjy_client = ChaojiyingClient('wlccgp3', 'wlcc1991', '897109')


if __name__ == '__main__':
    im = open('/Users/wanli/Documents/collector/miles/spider/liepin/18681441681.png', 'rb').read()
    print(cjy_client.PostPic(im, 9104))

