from fastapi import APIRouter, HTTPException, Depends
from database.connection import subscribers_collection, users_collection
from datetime import datetime

from models.email import EmailSchema

# FastAPI router
email_router = APIRouter()


@email_router.post("/subscribe")
def subscribe_user(request: EmailSchema):
    email = request.email.lower()
    existing_user = subscribers_collection.find_one({"email": email})
    user_already_in_db = users_collection.find_one({"email": email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already subscribed.")

    subscribers_collection.insert_one({
        "email": email,
        "is_subscribed": True,
        "date_subscribed": datetime.utcnow()
    })
    if user_already_in_db:
        users_collection.update_one(
            {"email": email},
            {"$set": {"is_subscribed": True}}
        )
    else:
        users_collection.insert_one({
            "email": email,
            "is_subscribed": True,
            "date_subscribed": datetime.utcnow()
        })

    return {"message": "Subscription successful!"}


# @email_router.delete("/unsubscribe")
# async def unsubscribe(email_data: EmailSchema):
#     email = email_data.email
#
#     result = subscribers_collection.delete_one({"email": email})
#     update_email = users_collection.update_one(
#         {"email": email},  # Replace <target_email> with the email you're targeting
#         {"$set": {"is_subscribed": False}}
#     )
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Email not found in the subscription list")
#
#     return {"message": "Successfully unsubscribed", "email": email}
