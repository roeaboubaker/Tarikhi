from sqlalchemy import Column, String, Integer, ForeignKey, TEXT, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid


class Story(Base):
    __tablename__ = "stories"

    story_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.site_id", ondelete = "CASCADE"), nullable = False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete = "SET NULL"), nullable = True)
    title = Column(String(255), nullable=False)
    summary = Column(TEXT)
    full_text = Column(TEXT)
    audio_url = Column(String(255))
    author = Column(String(255))
    source = Column(String(255))
    type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    site = relationship("Site", back_populates="stories")
    user = relationship("User")