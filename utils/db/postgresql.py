# -*- coding: utf-8 -*-

# @File   : postgresql.py
# @Author : Yuvv
# @Date   : 2018/5/4


from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

import settings


def get_db_engine():
    engine = create_engine(settings.SQLALCHEMY_URL)
    return engine


def get_db_session_factory(db_engine=None):
    if db_engine is None:
        db_engine = get_db_engine()
    session_factory = sessionmaker(bind=db_engine)
    return session_factory
