from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from internal.model.model import UserGroup
from internal.utils.xhs_helper import xhs_helper, CURRENT_USER_ID
from worker import engine


def save_user_groups():
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


if __name__ == "__main__":
    save_user_groups()
