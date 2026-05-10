# RecruitRadar

A personal tool I built to stop wasting time scrolling LinkedIn looking for real hiring posts. It runs daily, filters out all the engagement bait and fake "urgent requirement" posts, and drops only the real ones into a clean dashboard where I can track who I've reached out to.

**Live demo:** [recruitradar.onrender.com](https://recruitradar.onrender.com/)

![RecruitRadar Dashboard](https://res.cloudinary.com/dp8wy3ooi/image/upload/v1778407656/Screenshot_2026-05-10_153618_bnk4mv.png)

---

## What it does

Every day at 9 AM, the scheduler pulls fresh LinkedIn posts using Apify, sends them through Groq's LLM to separate the real job posts from spam, and saves only the genuine ones to MongoDB. The Streamlit dashboard then shows everything grouped by date — recruiter name, company, contact info, and a button to mark when you've sent a connection request.

The main problem it solves: LinkedIn is full of "Comment YES to get the JD" and "DM me urgently" posts that waste your time. This filters all of that out automatically.

---

## Stack

- **Scraping** — Apify (LinkedIn post scraper)
- **Filtering** — Groq API with Llama 3.3 70B
- **Storage** — MongoDB Atlas
- **Dashboard** — Streamlit with custom dark-mode CSS
- **Automation** — GitHub Actions (runs daily, completely free)
- **Hosting** — Render

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/manohar1030/RecruitRadar.git
cd RecruitRadar
pip install -r requirements.txt
```

### 2. Create a `.env` file

```env
APIFY_TOKEN=your_apify_token
APIFY_TASK_ID=your_task_id
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will be live at `http://localhost:8501`.

---

## Running with Docker

Spins up the dashboard and a local MongoDB instance together:

```bash
docker-compose up -d --build
```

Open `http://localhost:8501` once it starts.

---

## Automated scheduling via GitHub Actions

The `.github/workflows/scheduler.yml` file handles running the scraper daily at 9 AM IST on GitHub's free servers. To set it up on your own fork:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these four secrets: `MONGODB_URI`, `APIFY_TOKEN`, `APIFY_TASK_ID`, `GROQ_API_KEY`
3. Push to `main` — the workflow activates automatically

You can also trigger it manually from the **Actions** tab at any time.

---

## Project structure

```
RecruitRadar/
├── app.py              # Streamlit dashboard
├── scraper.py          # Apify scraper integration
├── ai_filter.py        # Groq LLM post filtering
├── storage.py          # MongoDB read/write
├── scheduler.py        # One-shot daily job script
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── scheduler.yml
```