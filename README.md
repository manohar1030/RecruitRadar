# 🎯 RecruitRadar

An AI-powered automation pipeline that scours LinkedIn for real hiring posts, intelligently filters out engagement bait using LLMs (Groq), and presents high-quality leads in a stunning, dark-mode glassmorphism dashboard.

## ✨ Features
- **🤖 AI-Powered Filtering:** Uses Groq to separate REAL job posts from FAKE engagement bait.
- **🌌 Premium Dashboard:** A sleek, interactive Streamlit UI featuring glassmorphism and modern typography.
- **✅ Lead Management:** Track outreach status (Pending/Sent) for each recruiter.
- **🔍 Smart Search:** Instantly find leads by recruiter name or company.
- **💾 MongoDB Storage:** Robust local data persistence for all your leads.
- **🐳 Fully Dockerized:** Spin up the UI, background scheduler, and database with a single command.

---

## 🚀 Quick Start (Docker - Recommended)

The easiest way to run RecruitRadar is using Docker Compose, which automatically sets up the UI, the daily scheduler, and a local MongoDB instance.

### 1. Configure Environment Variables
Create a `.env` file in the root directory:
```env
APIFY_TOKEN=your_apify_token
APIFY_TASK_ID=your_task_id
GROQ_API_KEY=your_groq_api_key
# MONGODB_URI is automatically handled by Docker, but you can override it here if using Atlas
```

### 2. Start the Stack
Run the following command to build and start all services:
```bash
docker-compose up -d --build
```

### 3. Access the Dashboard
Open your browser and navigate to:
**http://localhost:8501**

---

## 💻 Manual Setup (Without Docker)

If you prefer to run the components manually:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MongoDB
Ensure you have MongoDB running locally on port `27017` or add your connection string to the `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/linkedin_tracker
```

### 3. Run the Scheduler
The scheduler runs in the background and fetches new posts daily at 9:00 AM.
```bash
python scheduler.py
```

### 4. Run the Dashboard
In a separate terminal, launch the UI:
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Custom CSS (Glassmorphism)
- **Backend Pipeline:** Python, Schedule
- **Scraping:** Apify
- **AI Intelligence:** Groq (Llama Models)
- **Database:** MongoDB
- **Infrastructure:** Docker & Docker Compose