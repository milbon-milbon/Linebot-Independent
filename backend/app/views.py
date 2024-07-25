from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from pydantic import BaseModel
from app.services.conversation_service import save_conversation_history, get_conversation_history
from app.logging_config import logger


router = APIRouter()

init_db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# class Conversation(BaseModel):
#     user_id: str
#     message: str

# 履歴保存
@router.post("/conversation/")
async def create_conversation(
    user_id: str = Body(...),
    user_message: str = Body(...),
    bot_response: str = Body(...),
    db: Session = Depends(get_db)
):
    logger.debug("🚥create_conversationが呼び出されました")
    conversation = save_conversation_history(db, user_id, user_message, bot_response)
    logger.debug(f"🚥user_id:{user_id}")
    logger.debug(f"🚥user_message:{user_message}")
    logger.debug(f"🚥bot_response:{bot_response}")
    logger.debug(f"🚥db:{db}")
    logger.debug(f"🚥conversation:{conversation}")

    logger.debug("🚥正常にcreate_conversationが処理を終えそうです")
    return {
        "status": "success",
        "saved_conversation": conversation
    }
# async def create_conversation(user_id: str, user_message: str, bot_response: str, db: Session = Depends(get_db)):
#     conversation = save_conversation_history(db, user_id, user_message, bot_response)
#     # return conversation
#     return {
#         "status": "success",
#         "saved_conversation": conversation
#     }

# 特定ユーザーの履歴取得
@router.get("/conversation/{user_id}")
async def read_conversation(user_id: str, db: Session = Depends(get_db)):
    logger.debug(f"🚥read_conversationが呼び出されました")
    conversation = get_conversation_history(db, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    logger.debug("🚥正常にread_conversationの処理を終えそうです")
    return conversation
