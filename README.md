# 💼 LinkedIn Hiring Tracker

An AI-powered automation that finds real hiring posts on LinkedIn daily and displays them in a clean dashboard.

## Features
- 🤖 AI filters REAL vs FAKE hiring posts
- 📊 Clean Streamlit dashboard
- ✅ Mark sent/unsent for each recruiter
- 🔍 Search by name or company
- 📅 Grouped by date
- 💾 Persistent local storage

## Setup

### 1. Clone and install
```bash
pip install -r requirements.txt
```

### 2. Add your API keys
Create a `.env` file:
```
APIFY_TOKEN=your_apify_token
APIFY_TASK_ID=your_task_id
GROQ_API_KEY=your_groq_api_key
```

### 3. Run the scheduler (fetches posts daily at 9 AM)
```bash
python scheduler.py
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

## Deploy on Render
1. Push to GitHub
2. Create new Web Service on Render
3. Set environment variables
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port $PORT`

## Tech Stack
- Python
- Streamlit
- Apify (LinkedIn scraping)
- Groq AI (post filtering)
- JSON (local storage)