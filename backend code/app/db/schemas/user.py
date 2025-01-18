from pydantic import BaseModel
import uuid

class User(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str
    role:str 

class UserCreate(BaseModel):
    username: str
    email: str
    password:str
  
    