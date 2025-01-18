
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from app.db import database
from app.db.schemas import artifact as artifact_schema
from sqlalchemy.orm import Session
from app.db.models import Artifact, Site
from app.api.auth import get_current_user

router = APIRouter(tags = ["artifacts"])

@router.get("/artifacts", response_model=List[artifact_schema.Artifact])
async def get_all_artifacts(db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        artifacts = db.query(Artifact).all()
        return artifacts
    except Exception as ex:
         raise HTTPException(status_code=500, detail=str(ex))

@router.get("/artifacts/{artifact_id}", response_model=artifact_schema.Artifact)
async def get_artifact_by_id(artifact_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
         artifact = db.query(Artifact).filter(Artifact.artifact_id == artifact_id).first()
         if artifact:
            return artifact
         else:
            raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as ex:
          raise HTTPException(status_code=500, detail=str(ex))

@router.post("/artifacts", response_model=artifact_schema.Artifact, status_code = 201)
async def create_artifact(artifact_data: artifact_schema.ArtifactCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
      try:
         if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
         new_artifact = Artifact(**artifact_data.model_dump(), artifact_id= uuid.uuid4())
         db.add(new_artifact)
         db.commit()
         db.refresh(new_artifact)
         return new_artifact
      except Exception as ex:
         db.rollback()
         raise HTTPException(status_code=500, detail=str(ex))

@router.put("/artifacts/{artifact_id}", response_model=artifact_schema.Artifact)
async def update_artifact(artifact_id: uuid.UUID, artifact_data: artifact_schema.ArtifactCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        artifact = db.query(Artifact).filter(Artifact.artifact_id == artifact_id).first()
        if artifact:
           for key, value in artifact_data.model_dump(exclude_unset = True).items():
             setattr(artifact,key,value)
           db.commit()
           db.refresh(artifact)
           return artifact
        else:
           raise HTTPException(status_code=404, detail="Artifact not found")

    except Exception as ex:
       db.rollback()
       raise HTTPException(status_code=500, detail=str(ex))

@router.delete("/artifacts/{artifact_id}", status_code=204)
async def delete_artifact(artifact_id: uuid.UUID, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        if user.role != "admin":
             raise HTTPException(status_code=403, detail = "User does not have authorization")
        artifact = db.query(Artifact).filter(Artifact.artifact_id == artifact_id).first()
        if artifact:
            db.delete(artifact)
            db.commit()
            return
        else:
            raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/artifacts/name/{site_name}", response_model=artifact_schema.Artifact, status_code = 201)
async def create_artifact_by_site_name(site_name: str, artifact_data: artifact_schema.ArtifactCreate, db: Session = Depends(database.get_db), user = Depends(get_current_user)):
    try:
        site = db.query(Site).filter(Site.name == site_name).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
        new_artifact = Artifact(**artifact_data.model_dump(exclude={"site_id"}), site_id= site.site_id, artifact_id= uuid.uuid4())
        db.add(new_artifact)
        db.commit()
        db.refresh(new_artifact)
        return new_artifact
    except Exception as ex:
         db.rollback()
         raise HTTPException(status_code=500, detail=str(ex))