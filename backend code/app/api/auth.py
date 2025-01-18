from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.db import database
from app.db.models import User
from app.db.schemas import user as user_schema
from jose import jwt
from app.config import Config
import uuid
from fastapi.security import OAuth2PasswordBearer
import os


router = APIRouter(prefix = "/auth", tags = ["auth"])

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                  db: Session = Depends(database.get_db)):
  user = db.query(User).filter(User.username == form_data.username).first()
  if not user:
      raise HTTPException(status_code = 400, detail = "Incorrect username or password")
  if not user.verify_password(form_data.password):
      raise HTTPException(status_code = 400, detail = "Incorrect username or password")
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
  return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token")), 
                           db: Session = Depends(database.get_db)):
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username: str = payload.get("sub")
         role : str = payload.get("role")
         if username is None:
             raise HTTPException(status_code = 401, detail= "could not validate credentials")
     except Exception as ex:
          raise HTTPException(status_code = 401, detail= "could not validate credentials")
     user = db.query(User).filter(User.username == username).first()
     if not user:
        raise HTTPException(status_code=404, detail="User not found")
     user.role = role 
     return user