
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from app.db import database
from app.db.schemas import audio as audio_schema
from sqlalchemy.orm import Session
from app.db.models import Audio, Site
from app.api.auth import get_current_user

router = APIRouter(tags = ["audio"])


@router.get("/audio", response_model=List[audio_schema.Audio])
async def get_all_audio_files(db: Session = Depends(database.get_db), 
                              user = Depends(get_current_user)):
    try:
        audio_files = db.query(Audio).all()
        return audio_files
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))




@router.post("/audio", response_model=audio_schema.Audio, status_code = 201)
async def create_audio(audio_data: audio_schema.AudioCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
     try:
          if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
          new_audio = Audio(**audio_data.model_dump(), audio_id = uuid.uuid4())
          db.add(new_audio)
          db.commit()
          db.refresh(new_audio)
          return new_audio
     except Exception as ex:
          db.rollback()
          raise HTTPException(status_code=500, detail=str(ex))

@router.put("/audio/{audio_id}", response_model=audio_schema.Audio)
async def update_audio(audio_id: uuid.UUID, audio_data: audio_schema.AudioCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        audio = db.query(Audio).filter(Audio.audio_id == audio_id).first()
        if audio:
           for key, value in audio_data.model_dump(exclude_unset = True).items():
             setattr(audio,key,value)
           db.commit()
           db.refresh(audio)
           return audio
        else:
           raise HTTPException(status_code=404, detail="Audio not found")

    except Exception as ex:
       db.rollback()
       raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/audio/{audio_id}", status_code=204)
async def delete_audio(audio_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        audio = db.query(Audio).filter(Audio.audio_id == audio_id).first()
        if audio:
            db.delete(audio)
            db.commit()
            return
        else:
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))