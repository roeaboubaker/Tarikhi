
from pydantic import BaseModel
from typing import List
import uuid

class Audio(BaseModel):
    audio_id: uuid.UUID
    site_id: uuid.UUID
    audio_url: str
    title: str | None = None
    duration: int | None = None
    transcripts: str | None = None
    user_id: uuid.UUID | None = None

class AudioCreate(BaseModel):
    site_id: uuid.UUID | None = None
    audio_url: str
    title: str | None = None
    duration: int | None = None
    transcripts: str | None = None