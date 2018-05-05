# -*- coding: utf-8 -*-

# @File   : task.py
# @Author : Yuvv
# @Date   : 2018/5/5

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, VARCHAR, TIMESTAMP, Index, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class MLPMTaskFunc(BaseModel):
    __tablename__ = 'mlpm_task_func'

    creator = Column(String(128), comment='创建/提交这个函数的人名')
    name = Column(String(128), unique=True, comment='函数名称，格式为 module:name')
    desc = Column(VARCHAR(1023), comment='函数描述信息')
    doc = Column(VARCHAR(65535), comment='函数文档，主要是参数描述信息')
    pub_date = Column(TIMESTAMP, default=datetime.utcnow, comment='发布时间')


class UserTask(BaseModel):
    __tablename__ = 'user_task'

    username = Column(String(128), nullable=True)
    func_id = Column(BigInteger, ForeignKey('mlpm_task_func.id', ondelete='SET NULL'))
    task_id = Column(String(64), nullable=False, index=True)
    args = Column(VARCHAR(1023), nullable=True)
    kwargs = Column(VARCHAR(1023), nullable=True)
    desc = Column(VARCHAR(1023), nullable=True)
    create_date = Column(TIMESTAMP, default=datetime.utcnow)

    func = relationship(MLPMTaskFunc, foreign_keys=[func_id])

    __table_args__ = (Index('ix_username_create_date', 'username', 'create_date'),
                      UniqueConstraint('username', 'task_id'))
