from sqlalchemy.orm import Session
from models import Message, User

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, telegram_id: int, text: str):
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            return None

        new_message = Message(user_id=user.id, text=text)
        self.db.add(new_message)
        self.db.commit()
        return new_message

    def get_chat_history(self, telegram_id: int):
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            return None

        return self.db.query(Message).filter(Message.user_id == user.id).all()
