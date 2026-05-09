import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def clean_text(text):
    """Clean post text to avoid JSON issues"""
    if not text:
        return ""
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace('"', "'")
    text = text.replace("\\", " ")
    text = re.sub(r'[^\x20-\x7E]', ' ', text)
    return text[:1500]  # Limit length


def analyze_post(post):
    """Send post to Groq AI and get structured data"""

    cleaned_text = clean_text(post.get("text", ""))

    if not cleaned_text:
        return None

    system_prompt = """You analyze LinkedIn posts for hiring. Reply in JSON only. No markdown. No extra text.
Format exactly like this:
{"verdict": "REAL" or "FAKE", "posterName": "name of person or company who posted", "jobCompany": "company name mentioned in job description", "profileUrl": "linkedin profile url of poster", "contactInfo": "any email address or phone number or careers page url found in post, empty string if none"}

REAL post has: proper job description, role, skills, experience, company name, official contact.
FAKE post has: DM me, comment YES, urgent requirement, gmail IDs, no job description, like and share."""

    user_prompt = f"Analyze this LinkedIn post: {cleaned_text}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 500,
        "temperature": 0
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )

        if response.status_code != 200:
            print(f"Groq error: {response.text}")
            return None

        content = response.json()["choices"][0]["message"]["content"]
        
        # Clean response and parse JSON
        content = content.strip()
        content = re.sub(r'```json|```', '', content).strip()
        
        result = json.loads(content)
        return result

    except Exception as e:
        print(f"AI analysis failed: {e}")
        return None


def filter_real_posts(posts, limit=2):
    """Filter posts through AI and return only REAL ones"""
    real_posts = []

    print(f"Analyzing {len(posts)} posts with Groq AI...")

    for i, post in enumerate(posts):
        if len(real_posts) >= limit:
            break

        print(f"  Checking post {i+1}/{len(posts)}...")
        result = analyze_post(post)

        if not result:
            continue

        if result.get("verdict") == "REAL":
            real_posts.append({
                "posterName": result.get("posterName", post.get("authorName", "Unknown")),
                "jobCompany": result.get("jobCompany", ""),
                "profileUrl": result.get("profileUrl", post.get("authorProfileUrl", "")),
                "postUrl": post.get("url", ""),
                "contactInfo": result.get("contactInfo", ""),
                "verdict": "REAL"
            })
            print(f"  REAL post found! ({len(real_posts)}/{limit})")
        else:
            print(f"  FAKE post skipped")

    print(f"Found {len(real_posts)} real hiring posts.")
    return real_posts