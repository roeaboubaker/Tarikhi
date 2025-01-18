from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    username = Column(String(255), nullable = False, unique = True)
    email = Column(String(255), nullable = False, unique = True)
    password_hash = Column(String(255), nullable = False)
    role = Column(String(50), default="user")  
    created_at = Column(DateTime(timezone=True), server_default = func.now())
    updated_at = Column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now())

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def hash_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
    def update_user_role(self, role: str):
        self.role = role