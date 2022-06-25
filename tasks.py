# coding:utf-8
"""
Created on 2015-11-20

@author: root
"""
from __future__ import absolute_import

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from internal.model.model import UserKeyword, User, CATCH_STATUS_DONE, CATCH_STATUS_ING, CATCH_STATUS_INIT, NoteKeyword
from internal.utils import xhs_spider
from internal.utils.xhs_helper import xhs_helper
from worker import app, engine, cache
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class CacheLockContext:

    def __int__(self, lock_key, expire=60):
        self.lock_key = lock_key
        self.expire = expire

    def __enter__(self):
        print('enter')
        if not get_lock(self.lock_key, self.expire):
            raise Exception('lock failed')

    def __exit__(self, exc_type, exc_value, exc_tb):
        print('exit')
        release_lock(self.lock_key)


def get_lock(lock_key, expire=60):
    if cache.setnx(lock_key, 1):
        cache.expire(lock_key, expire)
        return True
    return False


def release_lock(lock_key):
    cache.delete(lock_key)


class CacheLockWrap:
    """
    redis 锁装饰器
    @CacheLockWrap('test', expire=60)
    def test():
        print('test')
    """

    def __init__(self, lock_key, expire=60):
        self.lock_key = lock_key
        self.expire = expire

    def __call__(self, func):
        def f(*args, **kwargs):
            if get_lock(self.lock_key, self.expire):
                try:
                    return func(*args, **kwargs)
                finally:
                    release_lock(self.lock_key)
        f.__name__ = func.__name__
        return f


@app.task
def print_ok():
    """测试
    """
    with Session(engine) as session:
        print(session.query(UserKeyword).all())


def search_user(session: Session, user_keyword: UserKeyword):
    """查询用户
    """
    resp = xhs_spider.WhosecardXhsSpider.get_search_user(user_keyword.keyword, user_keyword.page_index)
    ok = resp.get('ok', False)
    if ok:
        data = resp.get('result', {}).get('data', {})
        users = data.get('users', [])
        if len(users) == 0:
            user_keyword.status = CATCH_STATUS_DONE
        for u in users:
            session.execute(insert(User).values(
                user_id=u.get('id', ''),
                red_id=u.get('red_id', ''),
                user_name=u.get('name', ''),
                image=u.get('image', ''),
            ).on_duplicate_key_update(user_name=u.get('name', '')))
        user_keyword.page_index += 1
        session.commit()


@app.task
@CacheLockWrap('cron_search_users', expire=60)
def cron_search_users():
    """定时搜索用户信息，入库
    """
    with Session(engine) as session:
        keyword = session.query(UserKeyword).filter(UserKeyword.status == 0).first()
        if keyword:
            search_user(session, keyword)


def search_group(session: Session, user: User):
    """查询用户群聊列表
    """
    resp = xhs_helper.get_user_groups(user.user_id)
    ok = resp.get('success', False)
    if ok:
        data = resp.get('data', {})
        public_list = data.get('public_list', [])
        user.group_count = len(public_list)
        user.status = CATCH_STATUS_DONE
        session.commit()


@app.task
@CacheLockWrap('cron_search_group', expire=60)
def cron_search_group():
    """定时搜索用户群聊列表，入库
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.status == 0).first()
        if user:
            search_group(session, user)


def search_note(session: Session, note_keyword: NoteKeyword):
    """查询用户笔记
    """
    resp = xhs_spider.WhosecardXhsSpider.get_search_notes(note_keyword.keyword, note_keyword.page_index)
    if resp.get('ok', False):
        data = resp.get('result', {}).get('data', {})
        items = data.get('items', [])
        if len(items) == 0:
            note_keyword.status = CATCH_STATUS_DONE
        for item in items:
            u = item.get('note', {}).get('user', {})
            # userid = item.get('note', {}).get('user', {}).get('userid', '')
            session.execute(insert(User).values(
                user_id=u.get('userid', ''),
                user_name=u.get('nickname', ''),
                image=u.get('images', ''),
            ).on_duplicate_key_update(user_name=u.get('nickname', '')))
            # userid = item.get('note', {}).get('user', {}).get('userid', '')
            # u_resp = xhs_spider.WhosecardXhsSpider.get_user_info(userid)
            # if u_resp.get('ok', False):
            #     u_data = u_resp.get('result', {}).get('data', {})
            #     session.execute(insert(User).values(
            #         user_id=u_data.get('userid', ''),
            #         red_id=u_data.get('red_id', ''),
            #         user_name=u_data.get('nickname', ''),
            #         image=u_data.get('images', ''),
            #     ).on_duplicate_key_update(user_name=u_data.get('nickname', '')))
        note_keyword.page_index += 1
        session.commit()


@app.task
@CacheLockWrap('cron_search_note', expire=60)
def cron_search_note():
    """定时搜索用户群聊列表，入库
    """
    logger.info("cron_search_note")
    with Session(engine) as session:
        keyword = session.query(NoteKeyword).filter(NoteKeyword.status == 0).first()
        print(keyword)
        if keyword:
            search_note(session, keyword)


@app.task
@CacheLockWrap('cron_user_padding', expire=60)
def cron_user_padding():
    """定时补全有效用户RedID信息（只补全有群聊的用户）
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.group_count > 0, User.red_id == '').order_by(User.id).first()
        if user:
            resp = xhs_spider.WhosecardXhsSpider.get_user_info(user.user_id)
            if not resp:
                user.red_id = "获取失败，需人工处理"
                session.commit()
            else:
                if resp.get('ok', False):
                    u = resp.get('result', {}).get('data', {})
                    user.red_id = u.get('red_id', '')
                    session.commit()




