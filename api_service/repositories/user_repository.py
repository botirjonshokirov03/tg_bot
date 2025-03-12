from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_telegram_id(self, telegram_id: int):
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()

    def create_user(self, telegram_id: int, username: str):
        new_user = User(telegram_id=telegram_id, username=username)
        self.db.add(new_user)
        self.db.commit()
        return new_user
