# coding:utf-8
"""
Created on 2022-06-19

@author: lanjinmin
"""
from worker import cache


def get_lock(lock_key, expire=60):
    if cache.setnx(lock_key, 1):
        cache.expire(lock_key, expire)
        return True
    return False
