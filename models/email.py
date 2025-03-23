from pydantic import BaseModel, EmailStr
class EmailSchema(BaseModel):
    email: EmailStr

class BlogSendEmailRequest(BaseModel):
    blog_title: str
    blog_summary: str
    blog_url: str