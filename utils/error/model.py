# -*- coding: utf-8 -*-

# @File   : model.py
# @Author : Yuvv
# @Date   : 2018/5/4


from enum import Enum


class MLPMJobErrorEnum(Enum):
    """
    错误类枚举 (错误码，简短描述信息，http 状态码)
    """
    SUCCESS = 0, 'OK', 200
    UNKNOWN_ERROR = 500, '未知错误。', 500
    PERMISSION_DENIED = 403, "权限不足。", 403
    METHOD_NOT_ALLOWED = 405, "不支持的请求。", 405
    UNAUTHORIZED = 401, "未认证。", 401
    NOT_FOUND = 404, "资源未找到。", 404

    FIELD_MISSING = 2000, "字段缺失。", 422
    WRONG_FIELD_TYPE = 2001, "字段类型错误。", 422
    NOT_ACCEPTABLE = 2100, "资源类型错误。", 406
    NOT_UNIQUE = 2101, '字段不唯一。', 422
    BAD_TOKEN = 2200, "Token 无效。", 401
    BAD_SIGNATURE = 2201, "签名无效。", 422
    BAD_TIMESTAMP = 2202, '时间戳无效。', 422
    URL_EXPIRED = 2203, 'URL 过期。', 422
    BAD_JSON = 2300, 'JSON 解析错误', 422
    # account
    USER_NOT_FOUND = 3000, "用户不存在。", 404
    WRONG_PASSWORD = 3001, "密码错误。", 401
    BAD_AVATAR_URL = 3002, '头像 URL 无效。', 422
    BAD_QR_CODE_URL = 3100, '二维码无效。', 422
    SMS_VCODE_ERROR = 3200, '发送验证法失败', 422
    SMS_VCODE_TOO_FAST = 3201, '操作过快', 403
    BAD_VERIFICATION_CODE = 3202, '验证码无效', 422
    PHONE_NUMBER_BIND = 3203, '手机号已绑定', 422
    # moment
    EMPTY_POST = 4000, '空内容。', 422
    BAD_POST_CONTENT = 4001, '内容不合法。', 422
    BAD_POST_PICTURE = 4002, '图片不合法。', 422
    EMPTY_COMMENT = 4100, '空评论。', 422
    BAD_COMMENT = 4101, '评论不合法。', 422
    BAD_COMMENT_CONTENT = 4102, '内容不合法。', 422


class MLPMJobException(Exception):
    def __init__(self, err: MLPMJobErrorEnum, detail=None, **kwargs):
        self.code, self.msg, self.status = err.value
        if detail:
            self.msg += '\n' + detail
        self.data = kwargs

    def __repr__(self):
        return f'Error {self.code}: ' + self.msg

    def to_dict(self):
        return {'code': self.code,
                'msg': self.msg,
                'data': self.data}

