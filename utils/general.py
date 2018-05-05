# -*- coding: utf-8 -*-

# @File   : general.py
# @Author : Yuvv
# @Date   : 2018/5/5


import sys
from importlib import import_module

from flask import Response, json

from utils.error import MLPMJobErrorEnum, MLPMJobException


def _get_type_name(class_type):
    if class_type == str:
        return 'string'
    if class_type == int:
        return 'integer'
    if class_type == float:
        return 'float'
    if class_type == bool:
        return 'boolean'
    if class_type == object:
        return 'object'
    if class_type == list:
        return 'array'

    return str(class_type)


def make_json_resp(data=None, status_code: int = 200) -> Response:
    """
    将字典数据转为JSON返回（正常返回数据，错误代码为 0 即成功）
    :param data: 需要返回的数据，默认 None
    :param status_code: http 状态码，默认 200
    :return: None
    """
    code, msg, status = MLPMJobErrorEnum.SUCCESS.value
    media = {'code': code,
             'msg': msg,
             'data': data}
    resp = Response(json.dumps(media, ensure_ascii=False),
                    status=status_code,
                    content_type='application/json; charset=utf-8')
    return resp


def get_param(query_dict, field, required=False, allowed=None,
              convert_to=None, default=None, force=False):
    """
    获取指定 HttpRequest.QueryDict 的某字段的值，若发生错误则终止响应
    :param query_dict: 指定的查询集，GET, POST, FILES 等
    :param field: 字段名
    :param required: 是否为必填
    :param allowed: 若此项不为 None 则参数的值只能选取 allowed（list）中的值
    :param force: 如果为 True，则发生任何错误都返回 None 而不是中断响应
    :param convert_to: 待转换的数据类型
    :param default: 如果非必填项且值无效则返回此默认值
    :return: 字段值
    """
    value = query_dict.get(field)
    if not value and required:
        if not force:
            raise MLPMJobException(MLPMJobErrorEnum.FIELD_MISSING,
                                   'Field "%s" is missing' % field)
        return None
    elif not value and not required:
        return default or None
    elif allowed is not None and value not in allowed:
        if not force:
            raise MLPMJobException(MLPMJobErrorEnum.WRONG_FIELD_TYPE,
                                   'Value of field "%(field)s" should be one of [%(allowed_values)s].' % {
                                       'field': field, 'allowed_values': ','.join(allowed)})
        return None
    if convert_to:
        try:
            return None if not value else convert_to(value)
        except:
            if not force:
                raise MLPMJobException(MLPMJobErrorEnum.WRONG_FIELD_TYPE,
                                       'Field "%(field)s" should be %(required_type)s.' % {
                                           'field': field, 'required_type': _get_type_name(convert_to)})
            else:
                return None
    else:
        return value.strip() if hasattr(value, 'strip') else value


def load_request_body(request=None, expected=object):
    """
    获取用户请求中的原始JSON数据
    :return: JSON字典
    """
    try:
        json_data = json.loads(request.body)
        if not isinstance(json_data, expected):
            raise MLPMJobException(MLPMJobErrorEnum.NOT_ACCEPTABLE,
                                   detail='expect %s but %s given' % (type(expected), type(json_data)))
        return json_data
    except Exception as ex:
        raise MLPMJobException(MLPMJobErrorEnum.NOT_ACCEPTABLE, detail=str(ex))


def import_object(absolute_name):
    """
    根据名字 import 对象
    :param absolute_name: 按照 module:name 的格式
    :return: 返回对应对象
    """
    try:
        module_name, obj_name = absolute_name.split(':')
        module = sys.modules.get(module_name, None)
        if not module:
            module = import_module(module_name)
        obj = getattr(module, obj_name)
        return obj
    except ValueError:
        raise MLPMJobException(MLPMJobErrorEnum.BAD_FUNC_NAME,
                               f'函数名`{absolute_name}`不正确，应该为 `module:name` 的形式。')
    except ModuleNotFoundError:
        raise MLPMJobException(MLPMJobErrorEnum.BAD_FUNC_NAME,
                               f'没有找到您的函数名`{absolute_name}`所对应的对象。')
    except AttributeError:
        raise MLPMJobException(MLPMJobErrorEnum.BAD_FUNC_NAME,
                               f'没有找到函数名`{absolute_name}`所对应的对象。')
