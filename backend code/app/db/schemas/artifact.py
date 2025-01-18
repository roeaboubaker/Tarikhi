
from pydantic import BaseModel
from typing import List
import uuid

class Artifact(BaseModel):
      artifact_id: uuid.UUID
      site_id: uuid.UUID
      name: str
      description: str | None = None
      image_url: str | None = None
      model_url: str | None = None
      user_id: uuid.UUID | None = None

class ArtifactCreate(BaseModel):
      site_id: uuid.UUID | None = None
      name: str
      description: str | None = None
      image_url: str | None = None
      model_url: str | None = None