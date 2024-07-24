from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base
from .services.conversation_service import save_conversation_history

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/conversation")
def log_conversation(user_id: str, message: str, db: Session = Depends(get_db)):
    return save_conversation_history(db, user_id, message)