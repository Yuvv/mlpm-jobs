# -*- coding: utf-8 -*-

# @File   : middleware.py
# @Author : Yuvv
# @Date   : 2018/5/5


import hashlib
import base64
from datetime import datetime

import settings
from utils.error import MLPMJobErrorEnum, MLPMJobException


def check_authorization(timestamp, authorization):
    utc_timestamp = datetime.utcnow().timestamp()

    if utc_timestamp - timestamp > 60:
        raise MLPMJobException(MLPMJobErrorEnum.REQUEST_EXPIRED)

    try:
        method, code = authorization.split(' ')   # ValueError
        if method != 'Basic':
            raise MLPMJobException(MLPMJobErrorEnum.UNAUTHORIZED,
                                   '暂时只接受 HTTP 基本认证方式。')
        up = base64.decodebytes(code.encode('utf-8')).decode('utf-8')     # ValueError
        username, password = up.split(':')        # ValueError
        _password = settings.AUTH_USERS.get(username)
        if _password is None:
            raise MLPMJobException(MLPMJobErrorEnum.UNAUTHORIZED,
                                   '用户名不存在。')
        md5 = hashlib.md5()
        md5.update(f'{_password}@{timestamp}'.encode('utf-8'))
        md5sum = md5.hexdigest()
        if md5sum != password:
            raise MLPMJobException(MLPMJobErrorEnum.UNAUTHORIZED,
                                   '密码错误。')
    except ValueError:
        raise MLPMJobException(MLPMJobErrorEnum.UNAUTHORIZED,
                               '`Authorization` 值不合法。')

