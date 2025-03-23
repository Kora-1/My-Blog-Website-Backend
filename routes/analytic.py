from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from database.connection import blogs_collection, analytics_collection

analytic_router = APIRouter()


def get_user_identifier(request: Request):
    """Extract IP and User-Agent to uniquely identify a user."""
    user_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "Unknown")
    return f"{user_ip}-{user_agent}"


@analytic_router.post("/blog-like/{title}", response_class=JSONResponse)
def update_blog_likes(title: str, request: Request):
    """
    Increments the like count of a blog only if the user hasn't liked it before.
    """
    try:
        blog = blogs_collection.find_one({"title": title}, {"_id": 1})
        if not blog:
            return JSONResponse(status_code=404, content={"error": "Blog not found"})

        user_id = get_user_identifier(request)
        blog_id = blog["_id"]

        if analytics_collection.find_one({"blog_id": blog_id, "user_id": user_id, "action": "like"}):
            return JSONResponse(status_code=400, content={"error": "You have already liked this blog."})


        blogs_collection.update_one({"_id": blog_id}, {"$inc": {"likes": 1}})
        analytics_collection.insert_one({"blog_id": blog_id, "user_id": user_id, "action": "like"})

        return JSONResponse(content={"message": "Like count updated successfully"})

    except PyMongoError as e:
        return JSONResponse(status_code=500, content={"error": "Database error", "details": str(e)})



@analytic_router.post("/blog-view/{title}", response_class=JSONResponse)
def update_blog_views(title: str, request: Request):
    """
    Increments the view count of a blog only if the user hasn't viewed it before.
    """
    try:
        blog = blogs_collection.find_one({"title": title}, {"_id": 1})
        if not blog:
            return JSONResponse(status_code=404, content={"error": "Blog not found"})

        blog_id = blog["_id"]
        blogs_collection.update_one({"_id": blog_id}, {"$inc": {"views": 1}})

        return JSONResponse(content={"message": "View count updated successfully"})

    except PyMongoError as e:
        return JSONResponse(status_code=500, content={"error": "Database error", "details": str(e)})

