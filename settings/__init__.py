# -*- coding: utf-8 -*-

# @File   : __init__.py
# @Author : Yuvv
# @Date   : 2018/5/4


try:
    from .local_settings import *
except ImportError:
    from .default import *
