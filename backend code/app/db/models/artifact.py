
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, TEXT, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Artifact(Base):
    __tablename__ = "artifacts"
    artifact_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.site_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(TEXT)
    image_url = Column(String(255))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete = "SET NULL"), nullable = True)
    model_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    site = relationship("Site")
    user = relationship("User")