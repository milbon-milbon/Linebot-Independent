from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from .database import Base

class ConversationHistory(Base):
    __tablename__ = 'conversation_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
