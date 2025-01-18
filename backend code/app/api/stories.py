
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from app.db import database
from app.db.schemas import story as story_schema
from sqlalchemy.orm import Session
from app.db.models import Story, Site, User
from app.api.auth import get_current_user

router = APIRouter(tags = ["stories"])

@router.get("/stories", response_model=List[story_schema.Story])
async def get_all_stories(db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        stories = db.query(Story).all()
        return stories
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/stories/{story_id}", response_model=story_schema.Story)
async def get_story_by_id(story_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        story = db.query(Story).filter(Story.story_id == story_id).first()
        if story:
           return story
        else:
            raise HTTPException(status_code=404, detail="Story not found")
    except Exception as ex:
       raise HTTPException(status_code=500, detail=str(ex))


@router.post("/stories/name/{site_name}", response_model=story_schema.Story, status_code = 201)
async def create_story_by_site_name(site_name: str, story_data: story_schema.StoryCreate,
        db: Session = Depends(database.get_db), user: User = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if not site:
          raise HTTPException(status_code=404, detail="Site not found")
        new_story = Story(**story_data.model_dump(exclude={"site_id"}), site_id= site.site_id,
                           user_id = user.user_id, story_id= uuid.uuid4())
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
        return new_story
    except Exception as ex:
         db.rollback()
         raise HTTPException(status_code=500, detail=str(ex))

@router.put("/stories/{story_id}", response_model=story_schema.Story)
async def update_story(story_id: uuid.UUID, story_data: story_schema.StoryCreate,
                        db: Session = Depends(database.get_db), 
                       user = Depends(get_current_user)):
    try:
        story = db.query(Story).filter(Story.story_id == story_id).first()
        if story:
           for key, value in story_data.model_dump(exclude_unset = True).items():
             setattr(story,key,value)
           db.commit()
           db.refresh(story)
           return story
        else:
           raise HTTPException(status_code=404, detail="Story not found")

    except Exception as ex:
       db.rollback()
       raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/stories/{story_id}", status_code=204)
async def delete_story(story_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        story = db.query(Story).filter(Story.story_id == story_id).first()
        if story:
            db.delete(story)
            db.commit()
            return
        else:
            raise HTTPException(status_code=404, detail="Story not found")
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))