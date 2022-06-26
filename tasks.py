# coding:utf-8
"""
Created on 2015-11-20

@author: root
"""
from __future__ import absolute_import

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from internal.model.model import UserKeyword, User, CATCH_STATUS_DONE, CATCH_STATUS_ING, CATCH_STATUS_INIT, NoteKeyword, \
    UserGroup, UserSubscribeSpider
from internal.utils.xhs_helper import xhs_helper, CURRENT_USER_ID
from internal.utils.xhs_spider import WhosecardXhsSpider
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
    resp = WhosecardXhsSpider.get_search_user(user_keyword.keyword, user_keyword.page_index)
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
    resp = WhosecardXhsSpider.get_search_notes(note_keyword.keyword, note_keyword.page_index)
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
        note_keyword.page_index += 1
        session.commit()


@app.task
@CacheLockWrap('cron_search_note', expire=60)
def cron_search_note():
    """定时搜索用户群聊列表，入库
    """
    with Session(engine) as session:
        keyword = session.query(NoteKeyword).filter(NoteKeyword.status == 0).first()
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
            resp = WhosecardXhsSpider.get_user_info(user.user_id)
            if not resp:
                user.red_id = "获取失败，需人工处理"
                session.commit()
            else:
                if resp.get('ok', False):
                    u = resp.get('result', {}).get('data', {})
                    user.red_id = u.get('red_id', '')
                    session.commit()


@app.task
@CacheLockWrap('cron_group_members', expire=60)
def cron_group_members():
    """定时搜索用户群聊列表，入库
    """
    with Session(engine) as session:
        group = session.query(UserGroup).filter(UserGroup.status == 0).first()
        if group:
            resp = xhs_helper.get_get_group_members(group.group_id)
            ok = resp.get('success', False)
            if ok:
                data = resp.get('data', {})
                user_list = data.get('user_infos', [])
                for u in user_list:
                    # 插入用户记录
                    session.execute(insert(User).values(
                        user_id=u.get('user_id', ''),
                        user_name=u.get('nickname', ''),
                        image=u.get('image', ''),
                    ).on_duplicate_key_update(user_id=u.get('user_id', '')))
                    # 插入用户关注
                    session.execute(insert(UserSubscribeSpider).values(
                        user_id=u.get('user_id', ''),
                    ).on_duplicate_key_update(user_id=u.get('user_id', '')))
                group.status = CATCH_STATUS_DONE
                session.commit()


@app.task
@CacheLockWrap('cron_user_subscribe', expire=60)
def cron_user_subscribe():
    """定时搜索用户关注列表，入库
    """
    with Session(engine) as session:
        spider = session.query(UserSubscribeSpider).filter(UserSubscribeSpider.status == 0).first()
        if spider:
            resp = WhosecardXhsSpider.get_user_followings(spider.user_id, cursor=spider.cursor)
            if not resp:
                spider.status = CATCH_STATUS_DONE
                session.commit()
            else:
                if resp.get('ok', False):
                    data = resp.get('result', {}).get('data', {})
                    has_more = data.get('has_more', False)
                    cursor = data.get('cursor', '')
                    users = data.get('users', [])
                    if not has_more:
                        spider.status = CATCH_STATUS_DONE
                    if cursor:
                        spider.cursor = cursor
                    for u in users:
                        # 插入用户记录
                        session.execute(insert(User).values(
                            user_id=u.get('userid', ''),
                            user_name=u.get('nickname', ''),
                            image=u.get('images', ''),
                        ).on_duplicate_key_update(user_id=u.get('userid', '')))
                    session.commit()


@app.task
@CacheLockWrap('cron_user_groups', expire=60)
def cron_user_groups():
    with Session(engine) as session:
        resp = xhs_helper.get_my_groups()
        ok = resp.get('success', False)
        if ok:
            data = resp.get('data', {})
            chats = data.get('chats', [])
            for c in chats:
                # 插入用户记录
                session.execute(insert(UserGroup).values(
                    user_id=CURRENT_USER_ID,
                    group_id=c.get('group_id', ''),
                    group_name=c.get('info', {}).get('group_name', ''),
                ).on_duplicate_key_update(group_id=c.get('group_id', '')))
            session.commit()