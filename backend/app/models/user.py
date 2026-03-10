from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    credits = relationship("UserCredits", back_populates="user", uselist=False)
    ai_requests = relationship("AIRequests", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    research_documents = relationship("ResearchDocument", back_populates="user")
    memories = relationship("UserMemory", back_populates="user")