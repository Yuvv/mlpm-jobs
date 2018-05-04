# -*- coding: utf-8 -*-

# @File   : celery.py
# @Author : Yuvv
# @Date   : 2018/5/4


from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

import settings

app = Celery(broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULT_BACKEND)

app.conf.timezone = settings.CELERY_TIMEZONE
app.conf.imports = settings.CELERY_IMPORTS

app.conf.beat_schedule = {
    'expire_notifications': {
        'task': 'tasks.beat.expire_notifications',
        'schedule': crontab(minute=33, hour=3),
        # 'args': (*args)
    }
}

if __name__ == '__main__':
    app.start()
