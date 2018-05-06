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
    r = {}
    for word in re.split(r'\s+', content):
        if r.get(word, None) is None:
            r[word] = 1
        else:
            r[word] += 1
    return r


@shared_task(base=MLPMAsyncTask)
def spark_word_count(file_path: str) -> dict:
    """
    简单的spark单词统计示例程序
    :param file_path: 要统计的文本文件路径
    :return: 统计结果字典
    """

    from operator import add as op_add
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("PythonWordCount").getOrCreate()

    lines = spark.read.text(file_path).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: re.split(r'\s+', x)) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(op_add)
    output = counts.collect()

    d = {}
    for word, count in output:
        d[word] = count

    spark.stop()

    return d

