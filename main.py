from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.blog import blog_router
from routes.analytic import analytic_router
from routes.email import email_router

app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://localhost:63343",
    "http://localhost:63342",
    "https://blogs.dishant.tech"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(blog_router)
app.include_router(analytic_router)
app.include_router(email_router)
