from pydantic import BaseModel
from typing import List
from datetime import datetime

class Blog(BaseModel):
    title: str
    content: str
    views: int = 0
    likes: int = 0
    date_created: datetime
    tags: List[str]