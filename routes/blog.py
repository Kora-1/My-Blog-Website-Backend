from pymongo import DESCENDING
from pymongo.errors import PyMongoError
from database.connection import blogs_collection
from database.connection import comments_collection
from models.comments import CommentSchema
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

blog_router = APIRouter()

@blog_router.get("/")
def root():
    return "API CREATED BY D"

@blog_router.get("/blogs-get-preview", response_class=JSONResponse)
def get_blog_previews():
    """
    Fetch a list of blog previews with title, description, summary, likes, views, and date_created.
    """

    blogs = list(
        blogs_collection.find(
            {},  # Fetch all blogs
            {"_id": 0, "title": 1, "summary": 1, "likes": 1, "views": 1, "date_created": 1}
        ).sort("date_created", DESCENDING)  # Sort by newest first
    )

    return JSONResponse(content=blogs)


@blog_router.get("/blog-get/{title}")
def get_blog(title: str):
    """
    Fetch a full blog post by its title and return the details as a structured dictionary.
    """
    blog = blogs_collection.find_one({"title": title}, {"_id": 0})

    if not blog:
        return JSONResponse(status_code=404, content={"error": "Blog not found"})

    blog_details = {
        "Blog_Title": blog.get("title", ""),
        "Published_date": blog.get("date_created", ""),
        "Likes": blog.get("likes", 0),
        "Views": blog.get("views", 0),
        "content": blog["content"]
    }
    return JSONResponse(content=blog_details)

@blog_router.post("/post-blog-comments", response_class=JSONResponse)
async def post_blog_comment(comment: CommentSchema, request: Request):
    """
    Store blog comments in MongoDB with additional metadata.
    """
    try:

        blog = blogs_collection.find_one({"title": comment.blog_title})
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        comment_doc = {
            "blog_id": blog["_id"],
            "blog_title": comment.blog_title,
            "name": comment.name,
            "email": comment.email or "Anonymous",
            "comment": comment.comment,
            "date": comment.date,
            "ip": comment.ip,
            "user_agent": comment.user_agent,
            "location": comment.location or "Location not available",
            "status": comment.status,
            "created_at": datetime.utcnow()
        }
        comments_collection.insert_one(comment_doc)

        return JSONResponse(content={"message": "Comment posted successfully!"}, status_code=201)

    except PyMongoError as e:
        return JSONResponse(status_code=500, content={"error": "Database error", "details": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Unexpected error", "details": str(e)})
