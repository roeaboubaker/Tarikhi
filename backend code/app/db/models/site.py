from sqlalchemy import Column, String, Integer, DECIMAL, TEXT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Site(Base):
    __tablename__ = "sites"

    site_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    description = Column(TEXT)
    opening_hours = Column(TEXT)
    accessibility_info = Column(TEXT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete = "SET NULL"), nullable = True)
    tour_url = Column(String(255))
    map_url = Column(String(255))
    past_image = Column(String(255))  
    now_image = Column(String(255)) 
    stories = relationship("Story", back_populates="site")
    audio_files = relationship("Audio", back_populates = "site")
    user = relationship("User")