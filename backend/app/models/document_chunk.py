from sqlalchemy import Column, Integer, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from datetime import datetime


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("research_documents.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(JSON)
    chunk_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("ResearchDocument", back_populates="chunks")