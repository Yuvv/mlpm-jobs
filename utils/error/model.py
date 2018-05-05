# -*- coding: utf-8 -*-

# @File   : model.py
# @Author : Yuvv
# @Date   : 2018/5/4


from enum import Enum


class MLPMJobErrorEnum(Enum):
    """
    错误类枚举 (错误码，简短描述信息，http 状态码)
    """
    # common
    SUCCESS = 0, 'OK', 200
    UNKNOWN_ERROR = 500, '未知错误', 500
    PERMISSION_DENIED = 403, "权限不足", 403
    METHOD_NOT_ALLOWED = 405, "不支持的请求", 405
    UNAUTHORIZED = 401, "未认证", 401
    NOT_FOUND = 404, "资源未找到", 404
    # data
    FIELD_MISSING = 2000, "字段缺失", 422
    WRONG_FIELD_TYPE = 2001, "字段类型错误", 422
    BAD_ARGUMENTS = 2002, '参数解析错误', 422
    REQUEST_EXPIRED = 2100, '请求已过期。', 422
    # func
    FUNC_NOT_FOUND = 3000, "函数不存在", 404
    ILLEGAL_FUNC = 3001, '非法函数', 403
    BAD_FUNC_NAME = 3002, '函数名错误', 422
    BAD_FUNC_PARAM = 3003, "函数参数错误", 422
    # task
    TASK_NOT_FOUND = 4000, '任务不存在', 400


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
