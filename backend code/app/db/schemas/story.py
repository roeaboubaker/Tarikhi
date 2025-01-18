
from pydantic import BaseModel
from typing import List
import uuid

class Story(BaseModel):
    story_id: uuid.UUID
    site_id: uuid.UUID
    user_id: uuid.UUID | None = None
    title: str
    summary: str | None = None
    full_text: str | None = None
    audio_url: str | None = None
    author: str | None = None
    source: str | None = None
    type: str

class StoryCreate(BaseModel):
    site_id: uuid.UUID | None = None
    title: str
    summary: str | None = None
    full_text: str | None = None
    audio_url: str | None = None
    author: str | None = None
    source: str | None = None
    type: str