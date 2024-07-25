from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from datetime import datetime
from .database import Base

class ConversationHistory(Base):
    __tablename__ = 'conversation_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

