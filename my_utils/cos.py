#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
from qcloud_cos import CosConfig, CosS3Client, CosServiceError, CosClientError


__all__ = ['cos_client', 'MAPPING', 'CosServiceError', 'CosClientError']

COS_APP_ID = '1251958897'
COS_SECRET_ID = os.environ.get('COS_SECRET_ID')
COS_SECRET_KEY = os.environ.get('COS_SECRET_KEY')
if COS_APP_ID is None or COS_SECRET_KEY is None:
    raise Exception('add COS_SECRET_ID and COS_SECRET_KEY to env')

COS_REGION = 'ap-guangzhou'
COS_BUCKETS = {
    'default': os.environ.get('COS_BUCKET') or 'jobs',
    'assets': os.environ.get('COS_BUCKET_ASSETS') or 'assets-stg'
}

# 获取配置对象
config = CosConfig(Appid=COS_APP_ID,
                   Region=COS_REGION,
                   Secret_id=COS_SECRET_ID,
                   Secret_key=COS_SECRET_KEY)
# 获取客户端对象
cos_client = CosS3Client(config)


MAPPING = {
    'doc': 'application/msword',
    'dot': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'dotx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'docm': 'application/vnd.ms-word.document.macroEnabled.12',
    'dotm': 'application/vnd.ms-word.template.macroEnabled.12',
    'xls': 'application/vnd.ms-excel',
    'xlt': 'application/vnd.ms-excel',
    'xla': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xltx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12',
    'xltm': 'application/vnd.ms-excel.template.macroEnabled.12',
    'xlam': 'application/vnd.ms-excel.addin.macroEnabled.12',
    'xlsb': 'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'ppt': 'application/vnd.ms-powerpoint',
    'pot': 'application/vnd.ms-powerpoint',
    'pps': 'application/vnd.ms-powerpoint',
    'ppa': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'potx': 'application/vnd.openxmlformats-officedocument.presentationml.template',
    'ppsx': 'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'ppam': 'application/vnd.ms-powerpoint.addin.macroEnabled.12',
    'pptm': 'application/vnd.ms-powerpoint.presentation.macroEnabled.12',
    'potm': 'application/vnd.ms-powerpoint.template.macroEnabled.12',
    'ppsm': 'application/vnd.ms-powerpoint.slideshow.macroEnabled.12',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'htm': 'text/html',
    'html': 'text/html'
}
