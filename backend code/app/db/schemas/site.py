from pydantic import BaseModel
from typing import List
import uuid

class Site(BaseModel):
    site_id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    description: str | None = None
    opening_hours: str | None = None
    accessibility_info: str | None = None
    user_id: uuid.UUID | None = None
  
    tour_url: str | None = None
    map_url: str | None = None
    past_image: str | None = None   
    now_image: str | None = None   

class SiteCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: str | None = None
    opening_hours: str | None = None
    accessibility_info: str | None = None
 
    tour_url: str | None = None
    map_url: str | None = None
    past_image: str | None = None   
    now_image: str | None = None   


class SiteUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    description: str | None = None
    opening_hours: str | None = None
    accessibility_info: str | None = None
  
    tour_url: str | None = None
    map_url: str | None = None
    past_image: str | None = None   
    now_image: str | None = None   