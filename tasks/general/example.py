# -*- coding: utf-8 -*-

# @File   : example.py
# @Author : Yuvv
# @Date   : 2018/5/5

import re

from celery import shared_task
from celery.utils.log import get_logger

from tasks.core import MLPMAsyncTask

LOGGER = get_logger('celery.MLPMAsyncTask')


@shared_task(base=MLPMAsyncTask)
def word_count(content: str) -> dict:
    """
    简单的单词统计示例程序
    :param content: 带统计单词的字串
    :return: 统计结果字典
    """
    LOGGER.error('test....')
    r = {}
    for word in re.split(r'\s+', content):
        if r.get(word, None) is None:
            r[word] = 1
        else:
            r[word] += 1
    return r

