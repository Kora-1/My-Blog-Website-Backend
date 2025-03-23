# from fastapi import APIRouter, HTTPException
# from models.email import BlogSendEmailRequest
# from models.subscriptionEmail import send_new_blog_email  # Import function from email service
#
# # Create API Router
# email_router = APIRouter()
#
# # Pydantic Model for Request Data
#
#
# @email_router.post("/send-blog-email")
# def send_blog_email(request: BlogSendEmailRequest):
#     """API endpoint to trigger email notifications for a new blog."""
#     try:
#         response = send_new_blog_email(request.blog_title, request.blog_summary, request.blog_url)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error sending emails: {e}")
#
#
# '''
#                     sample
# curl -X POST "http://127.0.0.1:8000/send-blog-email" \
#      -H "Content-Type: application/json" \
#      -d '{
#            "blog_title": "The Future of AI",
#            "blog_summary": "Discover how AI is shaping the future of technology...",
#            "blog_url": "https://yourblog.com/blog/future-of-ai"
#          }'
# '''