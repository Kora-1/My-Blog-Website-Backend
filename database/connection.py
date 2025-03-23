from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://accforapplinmongodb:adda1234@blog-cluster.ipqjv.mongodb.net/?retryWrites=true&w=majority&appName=blog-cluster")
client = MongoClient(MONGO_URI)
db = client["BlogsDB"]
blogs_collection = db["blogs"]
subscribers_collection = db["subscribers"]
users_collection = db["all_user"]
analytics_collection= db["analytics"]
comments_collection= db["blogComments"]