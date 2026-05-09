import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("APIFY_TASK_ID")

def run_apify_scraper():
    print("Starting Apify scraper...")

    # Start the task
    run_url = f"https://api.apify.com/v2/actor-tasks/{TASK_ID}/runs?token={APIFY_TOKEN}"
    response = requests.post(run_url, json={"timeout": 60, "memory": 512})

    if response.status_code not in [200, 201]:
        print(f"Failed to start scraper: {response.text}")
        return []

    print("Waiting for scraper to finish (2 mins)...")
    time.sleep(120)

    # Get results
    results_url = f"https://api.apify.com/v2/actor-tasks/{TASK_ID}/runs/last/dataset/items?token={APIFY_TOKEN}"
    results = requests.get(results_url)

    if results.status_code != 200:
        print(f"Failed to get results: {results.text}")
        return []

    posts = results.json()
    print(f"Scraped {len(posts)} posts.")
    return posts


def extract_post_data(post):
    """Extract only needed fields from raw post"""
    return {
        "authorName": post.get("authorName", ""),
        "authorProfileUrl": post.get("authorProfileUrl", ""),
        "text": post.get("text", ""),
        "url": post.get("url", ""),
        "postedAtISO": post.get("postedAtISO", ""),
        "activityOfCompany": post.get("activityOfCompany", ""),
    }