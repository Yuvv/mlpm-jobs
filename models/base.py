# -*- coding: utf-8 -*-

# @File   : base.py
# @Author : Yuvv
# @Date   : 2018/5/4


from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    @property
    def pk(self):
        return self.id

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.pk)
