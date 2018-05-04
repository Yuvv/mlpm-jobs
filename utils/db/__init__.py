# -*- coding: utf-8 -*-

# @File   : __init__.py
# @Author : Yuvv
# @Date   : 2018/5/4


from sqlalchemy.orm import scoped_session

from .postgresql import get_db_session_factory


_pg_session_factory = get_db_session_factory()
PGSession = scoped_session(_pg_session_factory)

__all__ = [
    'PGSession',
]
