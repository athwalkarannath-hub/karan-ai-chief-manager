# Karan AI Chief Manager — Real V1 backend

This is a real runnable FastAPI application, not a static HTML demo.

## What it does now
- Persistent SQLite database
- Chief Manager command endpoint
- Optional OpenAI planning brain via `OPENAI_API_KEY`
- Tasks and execution records
- Owner approval gate for high-risk actions
- Agent registry with activation state
- Audit/activity logs
- Mobile browser dashboard

## Run
1. Install Python 3.11+.
2. Copy `.env.example` to `.env` and add your OpenAI key (optional for local rule-based mode; required for AI planning).
3. Run:
   `python -m venv .venv`
   `source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)
   `pip install -r requirements.txt`
   `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Open `http://SERVER-IP:8000` in Chrome.

## Important
This project does not autonomously access bank accounts, OTPs, passwords, payment accounts, or external customer systems. Those need explicit integrations and owner approval.
