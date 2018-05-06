# -*- coding: utf-8 -*-

# @File   : local_settings.example.py
# @Author : Yuvv
# @Date   : 2018/5/4


from .default import *


# secret key 在生产模式下最好更改下
# >>> import random
# >>> print(''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(48)]))
SECRET_KEY = 'el(a0w64aqs%7q-fuu@&kr_nw$($wczscvmo0r=cbi*5o)'

# 在生产模式下应设置为 False
DEBUG = False

# 有需要的话更改对应的用户名、密码、数据库名
# SQLALCHEMY_URL = 'postgresql+psycopg2://<username>:<password>@localhost:5432/<db_name>'


# 可以添加多个用户。生产模式下使用复杂一点的密码（虽然也并没什么卯月）
AUTH_USERS = {'yuvv': 'yuvv'}


# 有需要的话更改对应的用户名、密码、数据库名
# CELERY_BROKER_URL = 'amqp://<username>:<password>@localhost:5672/<vhost_name>'
# CELERY_RESULT_BACKEND = 'db+postgresql://<username>:<password>@localhost:5432/<db_name>'

# 可以如下方式修改 logging 参数
LOGGING['handlers']['file']['filename'] = '/var/log/mlpm-jobs/app.log'

