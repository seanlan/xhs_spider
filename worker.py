# coding:utf-8
"""
Created on 2015-11-20

@author: root
"""
import redis
from celery import Celery, platforms
from sqlalchemy import create_engine

platforms.C_FORCE_ROOT = True
app = Celery('xhs_spider', include=['tasks'])
app.config_from_object('config')
print(app.conf["SQLALCHEMY_DATABASE_URI"])
engine = create_engine(app.conf["SQLALCHEMY_DATABASE_URI"], encoding='utf8', echo=False, pool_pre_ping=True)
cache = redis.from_url(app.conf["REDIS_URI"])

if __name__ == '__main__':
    app.start()
