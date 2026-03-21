# 🎯 Freelancer Analyzer

An AI-powered intelligence platform that automatically scrapes, classifies, scores, and recommends freelance job opportunities across multiple platforms.

Built with **Python**, **PostgreSQL**, **LangChain + GPT-4o**, **ChromaDB**, **Apify**, **FastAPI**, and **Streamlit**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🕷️ **Multi-Source Scraping** | Upwork (via Apify Cloud Actors), RemoteOK (REST API), and extensible to Fiverr, Freelancer, etc. |
| 🤖 **LLM Job Classification** | GPT-4o-mini analyzes each job for difficulty, scam detection, core technologies, and hidden requirements. |
| 🧮 **Smart Scoring Engine** | Mathematical formula combining budget, client quality, competition level, and skill relevance. |
| 🔍 **Semantic Search (RAG)** | Describe your ideal job in natural language and find matches via ChromaDB vector similarity. |
| 📊 **Interactive Dashboard** | Streamlit-powered UI with trends, recommendations, client analysis, and AI search. |
| ⏰ **Autonomous Scheduler** | Set-and-forget daemon that runs the full pipeline every 2 hours automatically. |
| 🌐 **REST API** | FastAPI endpoints to integrate with external tools, bots, or browser extensions. |

---

## 🏗️ Architecture

```
Apify Cloud (Upwork) ─┐
RemoteOK API ─────────┤──▶ Pipeline ──▶ PostgreSQL
Fiverr (extensible) ──┘        │
                               ▼
                    LLM Classification (GPT-4o)
                               │
                               ▼
                    Scoring Engine + Trends
                               │
                        ┌──────┴──────┐
                        ▼             ▼
                   ChromaDB      Streamlit
                (Vector Search)  (Dashboard)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (via Docker recommended)
- API Keys: OpenAI, Apify

### 1. Clone & Install

```bash
git clone https://github.com/YOUR-USER/freelancer-analyzer.git
cd freelancer-analyzer
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your real API keys
```

### 3. Start PostgreSQL

```bash
docker run --name freelancer-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=freelancer_db \
  -p 5432:5432 \
  -d postgres
```

### 4. Run the Pipeline

```bash
# Scrape jobs from all sources
python main.py scrape

# Classify jobs with AI
python main.py analyze

# Score and rank jobs
python main.py score

# Aggregate skill trends
python main.py trends

# Generate vector embeddings for semantic search
python main.py embed

# Launch the dashboard
python main.py dashboard
```

### 5. Autopilot Mode 🛸

Run the full pipeline automatically every 2 hours:

```bash
python main.py scheduler
```

---

## 📁 Project Structure

```
freelancer_analyzer/
├── main.py                  # CLI entrypoint
├── config/
│   └── settings.py          # Environment & app configuration
├── database/
│   ├── db.py                # SQLModel engine & session
│   ├── models.py            # PostgreSQL schema (15+ tables)
│   ├── crud.py              # Data access layer
│   ├── seed.py              # Mock data generator
│   └── reset.py             # Database reset utility
├── scraper/
│   ├── upwork_scraper.py    # Apify Cloud Actor integration
│   ├── remoteok_scraper.py  # RemoteOK JSON API
│   ├── fiverr_scraper.py    # Fiverr scraper (extensible)
│   ├── pipeline.py          # Unified multi-source dispatcher
│   └── models.py            # Pydantic validation models
├── analytics/
│   ├── scoring.py           # Job scoring formula engine
│   ├── trends.py            # Skill trend aggregation
│   └── recommendations.py   # Hidden gems & top jobs logic
├── llm_analysis/
│   └── job_classifier.py    # LangChain + GPT-4o classification
├── rag/
│   ├── vector_store.py      # ChromaDB + OpenAI Embeddings
│   ├── embedder.py          # ETL: Postgres → ChromaDB
│   └── rag_query.py         # Semantic similarity search
├── api/
│   ├── app.py               # FastAPI server
│   └── routes_jobs.py       # REST endpoints
├── scheduler/
│   ├── cron.py              # APScheduler daemon
│   └── jobs.py              # Individual job functions
├── dashboard/
│   ├── app.py               # Streamlit main app
│   └── pages/               # Dashboard pages (trends, clients, recommendations)
└── requirements.txt
```

---

## 🛠️ Available Commands

| Command | Description |
|---|---|
| `python main.py scrape` | Scrape jobs from Upwork + RemoteOK |
| `python main.py analyze` | Run LLM classification on new jobs |
| `python main.py score` | Calculate scores for all jobs |
| `python main.py trends` | Aggregate skill trend statistics |
| `python main.py embed` | Generate ChromaDB vector embeddings |
| `python main.py dashboard` | Launch Streamlit dashboard |
| `python main.py api` | Start FastAPI REST server (port 8000) |
| `python main.py scheduler` | Start autonomous 2-hour pipeline loop |
| `python main.py reset` | Drop and recreate all database tables |
| `python main.py seed` | Populate database with mock data |

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `OPENAI_API_KEY` | ✅ | OpenAI API key for LLM + embeddings |
| `APIFY_API_KEY` | ✅ | Apify API key for Upwork scraping |
| `APIFY_ACTOR_ID` | ✅ | Apify Actor ID (e.g. `author/upwork-scraper`) |
| `APIFY_USER_ID` | ⬜ | Apify user ID |

---

## 📜 License

This project is for personal use and educational purposes.
