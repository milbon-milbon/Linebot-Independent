from sqlalchemy.orm import Session
from . import models

def save_conversation_history(db: Session, user_id: str, message: str):
    db_conversation = models.ConversationHistory(user_id=user_id, message=message)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation