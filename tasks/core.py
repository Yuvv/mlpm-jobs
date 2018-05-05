# -*- coding: utf-8 -*-

# @File   : core.py
# @Author : Yuvv
# @Date   : 2018/5/4

from importlib import import_module
from celery import shared_task
from celery.task import Task
from celery.utils.log import get_logger


LOGGER = get_logger('celery.MLPMAsyncTask')


class MLPMAsyncTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        LOGGER.error('execute task failed...', exc_info=True)


@shared_task(base=MLPMAsyncTask)
def do_async_task(func_module, func_name,
                  args: (list, tuple)=None, kwargs: dict=None):
    """
    异步执行未注册为 celery task 的任务（函数）
    :param func_module: 函数所在模块
    :param func_name: 函数名
    :param args: 参数，必须可被序列化为 json
    :param kwargs: 参数，必须可被序列化为 json
    :return: 返回函数执行结果
    :exception: ModuleNotFoundError, AttributeError
    """
    args = args or ()
    kwargs = kwargs or {}
    _module = import_module(func_module)
    func = getattr(_module, func_name)
    return func(*args, **kwargs)
