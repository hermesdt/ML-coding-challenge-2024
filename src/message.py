from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4, UUID
from datetime import datetime

class Message(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    position: int
    text: str
    created_at: datetime

class Summary(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    position: int
    text: str
    created_at: datetime
    message_ids: List[str]