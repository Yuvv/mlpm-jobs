# -*- coding: utf-8 -*-

# @File   : beat.py
# @Author : Yuvv
# @Date   : 2018/5/4

from celery.utils.log import get_logger

from .celery import app as celery_app


LOGGER = get_logger('celery.MLPMAsyncTask')


@celery_app.task
def beat_example():
    LOGGER.debug('example beat task!')
