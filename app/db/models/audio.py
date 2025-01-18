
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, TEXT, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.site_id", ondelete = "CASCADE"), nullable = False)
    audio_url = Column(String(255), nullable = False)
    title = Column(String(255))
    duration = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete = "SET NULL"), nullable = True)
    transcripts = Column(TEXT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    site = relationship("Site", back_populates="audio_files")
    user = relationship("User")