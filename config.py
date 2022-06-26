# coding:utf-8
"""
Created on 2015-11-20

@author: root
"""
from __future__ import absolute_import
import os
from dotenv import load_dotenv
from datetime import timedelta
from celery.schedules import crontab

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
BROKER_URL = os.getenv("CELERY_BROKER_URL")
REDIS_URI = os.getenv("REDIS_URI")

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 100
CELERY_IGNORE_RESULT = True

TASK_TIME_DELTA = 3600 * 10

CELERYBEAT_SCHEDULE = {  # 定时执行任务
    # 'print_ok': {
    #     'task': 'tasks.print_ok',
    #     'schedule': timedelta(seconds=5),  # 每5秒执行一次
    #     'args': (),
    # },
    # 'cron_search_users': {
    #     'task': 'tasks.cron_search_users',
    #     'schedule': timedelta(seconds=2),  # 每2秒执行一次
    #     'args': (),
    # },

    # 'cron_search_note': {
    #     'task': 'tasks.cron_search_note',
    #     'schedule': timedelta(seconds=1),  # 每2秒执行一次
    #     'args': (),
    # },
    'cron_search_group': {
        'task': 'tasks.cron_search_group',  # 获取用户拥有的群聊列表
        'schedule': timedelta(seconds=1),  # 每2秒执行一次
        'args': (),
    },
    'cron_user_padding': {
        'task': 'tasks.cron_user_padding',  # 获取用户信息（获取redid）
        'schedule': timedelta(seconds=1),  # 每1秒执行一次
        'args': (),
    },
    'cron_user_groups': {
        'task': 'tasks.cron_user_groups',   # 获取用户加入的群组
        'schedule': timedelta(seconds=300),  # 每300秒执行一次
        'args': (),
    },
    'cron_group_members': {
        'task': 'tasks.cron_group_members',    # 获取群组成员
        'schedule': timedelta(seconds=1),  # 每1秒执行一次
        'args': (),
    },
    'cron_user_subscribe': {
        'task': 'tasks.cron_user_subscribe',    # 获取用户关注的人
        'schedule': timedelta(seconds=1),  # 每1秒执行一次
        'args': (),
    }
}
