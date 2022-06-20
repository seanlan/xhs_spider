from sqlalchemy.orm import Session

import tasks
from internal.model.model import Base, User
from worker import engine

if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    with Session(engine) as session:
        user = session.query(User).filter(User.group_count > 0, User.red_id == '').order_by(User.id).first()
        print(user)

