from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from app.db import database
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from sqlalchemy import text

router = APIRouter(tags=["search"])

@router.get("/search", response_model=List[dict])
async def search_all(q: str, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    try:
        
        search_params = (f"%{q}%",) * 7
        
       
        results = db.execute(text("""
            SELECT 'site' AS type, site_id, name as title, description as summary 
            FROM sites 
            WHERE LOWER(name) LIKE LOWER(:search) OR LOWER(description) LIKE LOWER(:search)
            UNION ALL
            SELECT 'story' AS type, story_id, title, summary 
            FROM stories 
            WHERE LOWER(title) LIKE LOWER(:search) OR LOWER(summary) LIKE LOWER(:search) OR 
                                  LOWER(full_text) LIKE LOWER(:search)
            UNION ALL
            SELECT 'audio' AS type, audio_id, title, transcripts 
            FROM audio 
            WHERE LOWER(title) LIKE LOWER(:search) OR LOWER(transcripts) LIKE LOWER(:search)
        """), {"search": f"%{q}%"}).fetchall()
        
        
        search_list = [
            {"type": result[0], "id": result[1], "title": result[2], "summary": result[3]}
            for result in results
        ]
        
        return search_list

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
