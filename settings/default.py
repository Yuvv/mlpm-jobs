# -*- coding: utf-8 -*-

# @File   : default.py
# @Author : Yuvv
# @Date   : 2018/5/4

import os

# 工程目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = False


SQLALCHEMY_URL = 'postgresql+psycopg2://micl:micl@localhost:5432/mlpm_jobs'


AUTH_USERS = {'yuvv': 'yuvv'}


CELERY_BROKER_URL = 'amqp://micl:micl@localhost:5672/ziyan-server'
CELERY_RESULT_BACKEND = 'db+postgresql://micl:micl@localhost/mlpm_jobs_result   '
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = ('tasks.core',
                  'tasks.beat')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detail': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d %(funcName)s]'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',

        },
        'file': {
            'level': 'WARNING',
            'formatter': 'detail',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'flask.app': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
    }
}
