#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
from .logger import SHlogger

__all__ = ['YMClient']

logger = SHlogger(__name__).logger
TOKEN = '0088609006cf9a515390c4e8703c1b80bba3c695a401'
EXCLUDENO = '170.171.172.173.174.176.178.184.188'
CODE_MAPPING = {
    '1001': '参数token不能为空',
    '1002': '参数action不能为空',
    '1003': '参数action错误',
    '1004': 'token失效',
    '1005': '用户名或密码错误',
    '1006': '用户名不能为空',
    '1007': '密码不能为空',
    '1008': '账户余额不足',
    '1009': '账户被禁用',
    '1010': '参数错误',
    '1011': '账户待审核',
    '1012': '登录数达到上限',
    '2001': '参数itemid不能为空',
    '2002': '项目不存在',
    '2003': '项目未启用',
    '2004': '暂时没有可用的号码',
    '2005': '获取号码数量已达到上限',
    '2006': '参数mobile不能为空',
    '2007': '号码已被释放',
    '2008': '号码已离线',
    '2009': '发送内容不能为空',
    '2010': '号码正在使用中',
    '3001': '尚未收到短信',
    '3002': '等待发送',
    '3003': '正在发送',
    '3004': '发送失败',
    '3005': '订单不存在',
    '3006': '专属通道不存在',
    '3007': '专属通道未启用',
    '3008': '专属通道密码与项目不匹配',
    '9001': '系统错误',
    '9002': '系统异常',
    '9003': '系统繁忙',
}


class YMClient(object):
    def __init__(self, itemid):
        self.itemid = itemid

    def get_mobile(self):
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token={token}&itemid={itemid}&excludeno={excludeno}' \
            .format(token=TOKEN, itemid=self.itemid, excludeno=EXCLUDENO)
        try:
            response = requests.get(url).content.decode('utf-8')
        except Exception as e:
            logger.warning(e)
        else:
            if 'success' in response:
                mobile = response.split('|')[-1]
                return mobile
            else:
                logger.warning(CODE_MAPPING.get(response, response))

    def get_specified_mobile(self, mobile):
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token={token}&itemid={itemid}&mobile={mobile}&excludeno={excludeno}' \
            .format(token=TOKEN, itemid=self.itemid, mobile=mobile, excludeno=EXCLUDENO)
        try:
            response = requests.get(url).content.decode('utf-8')
        except Exception as e:
            logger.warning(e)
        else:
            if 'success' in response:
                mobile = response.split('|')[-1]
                return mobile
            elif response == '2010':
                logger.warning('{}: {}'.format(mobile, CODE_MAPPING.get(response, response)))
                return mobile
            else:
                logger.warning('{}: {}'.format(mobile, CODE_MAPPING.get(response, response)))

    def get_sms(self, mobile, release=0):
        count = 0
        while True:
            count += 1
            if count > 12:
                break
            url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token={token}&itemid={itemid}&mobile={mobile}&release={release}' \
                .format(token=TOKEN, itemid=self.itemid, mobile=mobile, release=release)
            try:
                response = requests.get(url).content.decode('utf-8')
            except Exception as e:
                logger.warning(e)
            else:
                if 'success' in response:
                    content = response.split('|')[-1]
                    return content
                elif response == '3001':
                    logger.warning('{}: {}'.format(mobile, CODE_MAPPING.get(response, response)))
                else:
                    return
            time.sleep(5)

    def release(self, mobile):
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token={token}&itemid={itemid}&mobile={mobile}' \
            .format(token=TOKEN, itemid=self.itemid, mobile=mobile)
        try:
            response = requests.get(url).content.decode('utf-8')
        except Exception as e:
            logger.warning(e)
        else:
            if response == 'success':
                logger.info('号码已释放: {}'.format(mobile))
            else:
                logger.warning('{}: {}'.format(mobile, CODE_MAPPING.get(response, response)))

    def release_all(self):
        url = 'http://api.fxhyd.cn/appapi.aspx?actionid=releaseall&token={token}' \
            .format(token=TOKEN)
        try:
            return requests.get(url).content.decode('utf-8')
        except Exception as e:
            logger.warning(e)

    def add_ignore(self, mobile):
        url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token={token}&itemid={itemid}&mobile={mobile}'\
                .format(token=TOKEN, itemid=self.itemid, mobile=mobile)
        try:
            response = requests.get(url).content.decode('utf-8')
        except Exception as e:
            logger.warning(e)
        else:
            if response == 'success':
                logger.info('号码已拉黑: {}'.format(mobile))
            else:
                logger.warning('{}: {}'.format(mobile, CODE_MAPPING.get(response, response)))


if __name__ == '__main__':
    yima_client = YMClient(itemid=3970)
    # phone = yima_client.get_mobile()
    # phone = yima_client.get_specified_mobile('18730746886')
    # captcha = yima_client.get_sms(phone, 1)
    # yima_client.release('17071721563')
    # yima_client.release_all()
    # yima_client.add_ignore('17076411317')
