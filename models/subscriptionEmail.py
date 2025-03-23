# import smtplib
# import os
# from pymongo import MongoClient
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from jinja2 import Template
#
# # MongoDB Connection
# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)
# db = client["blog_database"]
# subscribers_collection = db["subscribers"]
#
# # Email Configuration (Using Env Variables for Security)
# EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")  # Change to Yahoo if needed
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # 465 for SSL, 587 for TLS
# EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "your-email@gmail.com")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-email-password")
#
# # Jinja2 Email Template
# EMAIL_TEMPLATE = """
# <html>
# <body>
#     <h2>📢 New Blog Alert! 🚀</h2>
#     <p><strong>Title:</strong> {{ title }}</p>
#     <p><strong>Summary:</strong> {{ summary }}</p>
#     <p>👉 <a href="{{ blog_link }}" target="_blank"><strong>Read the full blog here</strong></a></p>
#     <hr>
#     <p>You are receiving this email because you subscribed to our blog updates.</p>
#     <p>❌ <a href="{{ unsubscribe_link }}" target="_blank">Unsubscribe</a></p>
# </body>
# </html>
# """
#
# def send_new_blog_email(blog_title, blog_summary, blog_url):
#     """Fetch subscribed emails and send them a notification about a new blog."""
#     subscribers = subscribers_collection.find({}, {"email": 1, "_id": 0})
#     email_list = [sub["email"] for sub in subscribers]
#
#     if not email_list:
#         print("No subscribers found.")
#         return
#
#     # SMTP Server Setup
#     try:
#         server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         server.starttls()
#         server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
#
#         for email in email_list:
#             unsubscribe_link = f"https://yourblog.com/unsubscribe?email={email}"
#
#             # Render Email Content
#             template = Template(EMAIL_TEMPLATE)
#             email_content = template.render(
#                 title=blog_title,
#                 summary=blog_summary,
#                 blog_link=blog_url,
#                 unsubscribe_link=unsubscribe_link
#             )
#
#             # Construct Email
#             message = MIMEMultipart()
#             message["From"] = EMAIL_USERNAME
#             message["To"] = email
#             message["Subject"] = f"🚀 New Blog Published: {blog_title}"
#             message.attach(MIMEText(email_content, "html"))
#
#             # Send Email
#             server.sendmail(EMAIL_USERNAME, email, message.as_string())
#
#         server.quit()
#         print("✅ Emails sent successfully!")
#
#     except Exception as e:
#         print(f"❌ Error sending emails: {e}")
