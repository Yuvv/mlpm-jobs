# -*- coding: utf-8 -*-

# @File   : default.py
# @Author : Yuvv
# @Date   : 2018/5/4

import os

# 工程目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'el(a0w64aqs%7hhq-fuu@&kr_nw$($wczscvmo0r=cbi*5o)'

DEBUG = False


SQLALCHEMY_URL = 'postgresql+psycopg2://micl:micl@localhost:5432/mlpm_jobs'


AUTH_USERS = {'yuvv': 'yuvv'}


CELERY_BROKER_URL = 'amqp://micl:micl@localhost:5672/ziyan-server'
CELERY_RESULT_BACKEND = 'db+postgresql://micl:micl@localhost/mlpm_jobs_result'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_IMPORTS = ('tasks.core',
                  'tasks.beat',
                  'tasks.general')

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
            'encoding': 'utf-8',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10
        },
        'celery.file': {
            'level': 'WARNING',
            'formatter': 'detail',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/celery/MLPMAsyncTask.log',
            'encoding': 'utf-8',
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
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False
        },
        'celery.MLPMAsyncTask': {
            'handlers': ['celery.file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}
