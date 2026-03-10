from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.app.core.database import Base
from datetime import datetime


class PromptPerformance(Base):
    __tablename__ = "prompt_performance"

    id = Column(Integer, primary_key=True, index=True)
    prompt_version = Column(String, nullable=False)
    token_usage = Column(Integer, default=0)
    response_time = Column(Float, default=0.0)
    user_rating = Column(Float, nullable=True)
    success_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)