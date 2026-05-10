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

    system_prompt = """You are an AI that extracts hiring information from LinkedIn posts.
Reply ONLY with a valid JSON object. No markdown formatting like ```json.
Format EXACTLY like this:
{
  "verdict": "REAL",
  "jobCompany": "Extracted company name (or empty string)",
  "contactInfo": "Extracted email, phone, application link, or 'DM the author'"
}

Criteria for REAL: Mention of hiring, job roles, skills, or asking for resumes.
Criteria for FAKE: "Comment YES", engagement bait, "like and share", unrelated content.

IMPORTANT for contactInfo: 
- Search thoroughly for ANY email address (e.g., @gmail.com, @company.com), phone number, or URL (e.g., bit.ly/..., forms.gle/..., company.com/careers).
- If the post explicitly says "DM me" or "Direct message", output "DM the author".
- Do not miss emails or links.
"""

    user_prompt = f"Analyze this LinkedIn post:\n{cleaned_text}"

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
            # Use raw post properties directly for profile and name,
            # rely on AI only for parsing company and contact.
            real_posts.append({
                "posterName": post.get("authorName", "Unknown"),
                "jobCompany": result.get("jobCompany", ""),
                "profileUrl": post.get("authorProfileUrl", ""),
                "postUrl": post.get("url", ""),
                "contactInfo": result.get("contactInfo", ""),
                "verdict": "REAL"
            })
            print(f"  REAL post found! ({len(real_posts)}/{limit})")
        else:
            print(f"  FAKE post skipped")

    print(f"Found {len(real_posts)} real hiring posts.")
    return real_posts