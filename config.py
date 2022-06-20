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
    'cron_search_note': {
        'task': 'tasks.cron_search_note',
        'schedule': timedelta(seconds=2),  # 每2秒执行一次
        'args': (),
    },
    # 'cron_search_users': {
    #     'task': 'tasks.cron_search_users',
    #     'schedule': timedelta(seconds=2),  # 每2秒执行一次
    #     'args': (),
    # },
    'cron_search_group': {
        'task': 'tasks.cron_search_group',
        'schedule': timedelta(seconds=1),  # 每2秒执行一次
        'args': (),
    },
    'cron_user_padding': {
        'task': 'tasks.cron_user_padding',
        'schedule': timedelta(seconds=1),  # 每2秒执行一次
        'args': (),
    },
}
