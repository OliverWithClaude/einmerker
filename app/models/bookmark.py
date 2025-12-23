from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    crawl_interval = Column(String(20), default="weekly", nullable=False)  # daily, weekly, monthly, once, never
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="bookmarks")
