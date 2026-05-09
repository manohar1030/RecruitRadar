import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

def get_collection():
    """Connect to MongoDB and return collection"""
    client = MongoClient(MONGODB_URI)
    db = client["linkedin_tracker"]
    return db["posts"]


def load_data():
    """Load all posts from MongoDB"""
    try:
        collection = get_collection()
        posts = list(collection.find({}, {"_id": 0}))
        return posts
    except Exception as e:
        print(f"MongoDB load error: {e}")
        return []


def save_post(post):
    """Save a single post to MongoDB"""
    try:
        collection = get_collection()
        collection.insert_one(post)
    except Exception as e:
        print(f"MongoDB save error: {e}")


def add_posts(new_posts):
    """Add new posts with today's date"""
    today = datetime.now().strftime("%d %b %Y")
    ist_time = datetime.now().strftime("%d/%m/%Y %H:%M")

    for post in new_posts:
        entry = {
            "id": f"{datetime.now().timestamp()}_{post.get('postUrl', '')[-10:]}",
            "date": today,
            "datetime": ist_time,
            "posterName": post.get("posterName", "Unknown"),
            "jobCompany": post.get("jobCompany", ""),
            "profileUrl": post.get("profileUrl", ""),
            "postUrl": post.get("postUrl", ""),
            "contactInfo": post.get("contactInfo", ""),
            "status": "unsent"
        }
        save_post(entry)

    print(f"Saved {len(new_posts)} posts to MongoDB.")


def update_status(post_id, status):
    """Update sent/unsent status"""
    try:
        collection = get_collection()
        collection.update_one(
            {"id": post_id},
            {"$set": {"status": status}}
        )
    except Exception as e:
        print(f"MongoDB update error: {e}")


def get_grouped_data():
    """Return posts grouped by date newest first"""
    data = load_data()

    grouped = {}
    for post in data:
        date = post["date"]
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(post)

    sorted_grouped = dict(
        sorted(
            grouped.items(),
            key=lambda x: datetime.strptime(x[0], "%d %b %Y"),
            reverse=True
        )
    )
    return sorted_grouped