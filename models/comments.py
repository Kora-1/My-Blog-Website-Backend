from pydantic import BaseModel, EmailStr
from typing import Optional

class CommentSchema(BaseModel):
    blog_title: str
    name: str
    email: Optional[EmailStr] = None
    comment: str
    date: str
    ip: str
    user_agent: str
    location: Optional[str] = None
    status: bool = True

