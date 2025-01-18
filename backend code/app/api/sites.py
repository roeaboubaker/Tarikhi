from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from app.db import database
from app.db.schemas import site as site_schema
from sqlalchemy.orm import Session
from app.db.models import Site
from app.api.auth import get_current_user
from app.db.schemas import story as story_schema
from app.db.schemas import audio as audio_schema
from app.db.models import Story, Audio
from app.db.models import User

router = APIRouter(tags = ["sites"])

@router.get("/sites", response_model=List[site_schema.Site])
async def get_all_sites(db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        sites = db.query(Site).all()
        return sites
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/sites/{site_id}", response_model=site_schema.Site)
async def get_site_by_id(site_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.site_id == site_id).first()
        if site:
             return site
        else:
            raise HTTPException(status_code=404, detail="Site not found")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/sites/name/{site_name}", response_model=site_schema.Site)
async def get_site_by_name(site_name: str, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
      try:
          site = db.query(Site).filter(Site.name == site_name).first()
          if site:
               return site
          else:
             raise HTTPException(status_code=404, detail="Site not found")
      except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
@router.post("/sites", response_model=site_schema.Site, status_code = 201)
async def create_site(site_data: site_schema.SiteCreate, db: Session = Depends(database.get_db),
                       user:User = Depends(get_current_user)):
      try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        new_site = Site(**site_data.model_dump(), site_id= uuid.uuid4())
        db.add(new_site)
        db.commit()
        db.refresh(new_site)
        return new_site
      except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/sites/name/{site_name}/description", response_model=str)
async def get_site_description_by_name(site_name: str, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if site:
             return site.description
        else:
             raise HTTPException(status_code=404, detail="Site not found")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
@router.get("/sites/name/{site_name}/map", response_model=str)
async def get_site_description_by_name(site_name: str, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if site:
             return site.map_url
        else:
             raise HTTPException(status_code=404, detail="Site not found")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/sites/name/{site_name}/stories", response_model=List[story_schema.Story])
async def get_site_stories_by_name(site_name: str, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if not site:
           raise HTTPException(status_code=404, detail="Site not found")
        stories = db.query(Story).filter(Story.site_id == site.site_id).all()
        return stories
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/sites/name/{site_name}/audio", response_model=List[audio_schema.Audio])
async def get_site_audio_by_name(site_name: str, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if not site:
           raise HTTPException(status_code=404, detail="Site not found")
        audio_files = db.query(Audio).filter(Audio.site_id == site.site_id).all()
        return audio_files
    except Exception as ex:
         raise HTTPException(status_code=500, detail=str(ex))
@router.put("/sites/{site_id}", response_model=site_schema.Site)
async def update_site(site_id: uuid.UUID, site_data: site_schema.SiteUpdate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        site = db.query(Site).filter(Site.site_id == site_id).first()
        if site is not None:
           for key, value in site_data.model_dump(exclude_unset = True).items():
             setattr(site,key,value)
           db.commit()
           db.refresh(site)
           return site
        else:
           raise HTTPException(status_code=404, detail="Site not found")

    except Exception as ex:
       db.rollback()
       raise HTTPException(status_code=500, detail=str(ex))