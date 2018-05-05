# -*- coding: utf-8 -*-

# @File   : celery.py
# @Author : Yuvv
# @Date   : 2018/5/4


from __future__ import absolute_import

import logging.config

from celery import Celery
from celery.schedules import crontab

import settings

logging.config.dictConfig(settings.LOGGING)

app = Celery(broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULT_BACKEND)
# app.config_from_object('settings')
app.conf.timezone = settings.CELERY_TIMEZONE
app.conf.imports = settings.CELERY_IMPORTS
# app.autodiscover_tasks('tasks')

app.conf.beat_schedule = {
    'example': {
        'task': 'tasks.beat.beat_example',
        'schedule': crontab(minute=33, hour=3),
        # 'args': (*args)
    }
}

if __name__ == '__main__':
    app.start()
