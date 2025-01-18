
from fastapi import APIRouter, HTTPException, Depends
from app.db import database
from app.db.models import User
from sqlalchemy.orm import Session
from app.db.schemas import user as user_schema
import uuid
from sqlalchemy.exc import IntegrityError
from app.db.models import User
from app.api.auth import get_current_user
router = APIRouter(tags = ["users"])

@router.post("/users", response_model=user_schema.User, status_code = 201)
async def create_user(user_data: user_schema.UserCreate, db: Session = Depends(database.get_db)):
    try:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code = 400, detail = "Username is already taken")
        new_user = User(**user_data.model_dump(exclude={"password"}), user_id= uuid.uuid4())
        new_user.hash_password(user_data.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as ex:
       db.rollback()
       raise HTTPException(status_code=400, detail = "Username already exists")

    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))
@router.get("/users", response_model=list[user_schema.User])
async def get_all_users(db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        users = db.query(User).all()
        return users
    except Exception as ex:
         raise HTTPException(status_code=500, detail=str(ex))