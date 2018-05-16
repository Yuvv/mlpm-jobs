# -*- coding: utf-8 -*-

# @File   : helper.py
# @Author : Yuvv
# @Date   : 2018/5/6


"""
完全是为了辅助使用本系统。
"""

from sqlalchemy.exc import DatabaseError

from models import MLPMTaskFunc
from utils.db import PGSession


def add_mlpm_task_func(func, description: str=None) -> dict:
    """
    添加一个任务函数
    :param func: 对应的任务函数对象
    :param description: 简短描述信息
    :return: 添加后的任务函数信息
    """
    session = PGSession()
    try:
        task_func = MLPMTaskFunc(name=f'{func.__module__}:{func.__name__}',
                                 desc=description,
                                 doc=func.__doc__)
        session.add(task_func)
        session.commit()
    except AttributeError:
        print('func 不合法')
    except DatabaseError as ex:
        print('添加失败', ex.args, ex.detail)
        session.rollback()
    else:
        return task_func.as_dict()
    finally:
        session.close()
