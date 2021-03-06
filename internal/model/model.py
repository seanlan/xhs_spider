# coding:utf-8
"""
Created on 2022-06-19

@author: lanjinmin
"""
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import registry

from worker import engine

CATCH_STATUS_INIT = 0  # 未处理
CATCH_STATUS_ING = 1   # 处理中
CATCH_STATUS_DONE = 2  # 处理完成

mapper_registry = registry()
Base = mapper_registry.generate_base()
mapper_registry.metadata.create_all(engine)


class UserKeyword(Base):
    """
    用户搜索关键字表
    """

    __tablename__ = 'user_keyword'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False)
    page_index = Column(Integer, nullable=False, default=0)    # 当前页码
    status = Column(Integer, nullable=False, default=0)        # 0:未处理，1:处理中 2:处理完成

    def __repr__(self):
        return '<UserKeyword %r>' % self.keyword


class NoteKeyword(Base):
    """
    笔记搜索关键字表
    """

    __tablename__ = 'note_keyword'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False)
    page_index = Column(Integer, nullable=False, default=0)  # 当前页码
    status = Column(Integer, nullable=False, default=0)  # 0:未处理，1:处理中 2:处理完成

    def __repr__(self):
        return '<NoteKeyword %r>' % self.keyword


class User(Base):
    """
    用户表
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    red_id = Column(String(50), nullable=False, default='')
    user_id = Column(String(50), nullable=False, unique=True, default='')
    user_name = Column(String(50), nullable=False, default='')
    image = Column(String(500), nullable=False, default='')
    group_count = Column(Integer, nullable=False, default=0)  # 群聊数量
    status = Column(Integer, nullable=False, default=0)    # 0:未处理，1:处理中 2:处理完成

    def __repr__(self):
        return '<User %r>' % self.user_id


class UserGroup(Base):
    """
    用户群聊表
    """

    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, default='')
    group_id = Column(String(50), nullable=False, unique=True)
    group_name = Column(String(50), nullable=False, default='')
    status = Column(Integer, nullable=False, default=0)    # 0:未处理，1:处理中 2:处理完成

    def __repr__(self):
        return '<UserGroup %r>' % self.group_id


class UserSubscribeSpider(Base):
    """
    用户订阅爬虫记录
    """

    __tablename__ = 'user_subscribe_spider'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, unique=True)
    cursor = Column(String(50), nullable=False, default='')
    status = Column(Integer, nullable=False, default=0)    # 0:未处理，1:处理中 2:处理完成

    def __repr__(self):
        return '<UserSubscribeSpider %r>' % self.spider_id

