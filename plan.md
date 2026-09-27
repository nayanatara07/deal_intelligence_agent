# Deal Intelligence Agent — Hackathon Plan

## One-Liner
**"An AI that remembers every call in a deal so a rep never walks into call #5 unprepared."**

## Tech Stack
- **Memory**: Hindsight (local server or Cloud)
- **LLM**: Groq (`openai/gpt-oss-120b`)
- **UI**: Streamlit
- **Database**: SQLite

## Architecture
```
[Transcript input] → [Groq LLM Extraction] → [Structured Facts]
                                                      ↓
                                          [Hindsight: retain memory]
                                                      ↓
[Next call trigger] → [Hindsight: recall] → [Groq LLM Brief Generation] → [Pre-call Brief UI]
```

## Project Structure
```
deal_intelligence_agent/
├── app.py                 # Streamlit UI
├── seed.py                # Database seeding + Hindsight processing
├── requirements.txt       # Dependencies
├── .env / .env.example    # API keys config
├── plan.md                # This file
├── data/
│   └── deals.db           # SQLite database
└── src/
    ├── config.py          # Hindsight + Groq config
    ├── database.py        # SQLite models
    ├── hindsight_layer.py # Hindsight integration
    ├── extraction.py      # LLM extraction pipeline
    ├── briefing.py        # Briefing generator
    └── synthetic_data.py  # Synthetic deal data
```

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/nayanatara07/deal_intelligence_agent.git
cd deal_intelligence_agent
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install hindsight-api
```

### 4. Get API Keys
- **Groq**: https://console.groq.com → free tier, no credit card needed
- **Hindsight**: https://ui.hindsight.vectorize.io → use promo code `MEMHACK99` for $50 free credits

### 5. Configure `.env`
Copy `.env.example` to `.env` and fill in:
```env
# Hindsight (local server)
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=http://localhost:8888
HINDSIGHT_BANK_ID=deal-intelligence

# Groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

# Database
DATABASE_PATH=data/deals.db
```

### 6. Start Hindsight Server (Terminal 1)
```cmd
set HINDSIGHT_API_LLM_API_KEY=your_groq_api_key
set HINDSIGHT_API_LLM_BASE_URL=https://api.groq.com/openai/v1
hindsight-api
```

### 7. Run the App (Terminal 2)
```bash
streamlit run app.py
```

### 8. Use the App
1. Click **"Seed Database"** in the sidebar
2. Select **"Nexus Analytics"** from the dropdown
3. Click **"Process with Hindsight"** — extracts facts from all calls and stores in memory
4. Go to **"Pre-Call Briefing"** tab
5. Click **"Generate Briefing with Memory"** — see what the agent remembers
6. Click **"Generate Briefing WITHOUT Memory"** — compare with generic advice

## Demo Flow (60-90 seconds)

1. **Set the scene (10s):** "You're an AE. You've had 4 calls with Nexus Analytics — a $250K HR tech deal. It's 5 minutes before call 5."

2. **Show the brief (20s):** Click "Generate Briefing with Memory" — surface a specific remembered detail (e.g., "Priya raised a security concern in call 2 that was never followed up on").

3. **Show it acting on memory (20s):** Ask the agent a question mid-"call" and show it answering from accumulated memory.

4. **Show the learning curve (20s):** Show cross-deal patterns — "The ROI calculator tactic worked in 3 other deals, use it again."

5. **Close (10s):** "Without memory, every call starts from zero. With memory, reps save 2-3 hours per week on prep."

## Synthetic Data

| Deal | Company | Value | Stage | Calls |
|------|---------|-------|-------|-------|
| Hero | Nexus Analytics | $250K | Negotiation | 5 |
| Background | Vertex Solutions | $180K | Closed Won | 3 |
| Background | Aurora Retail Group | $320K | Closed Won | 3 |
| Background | Pinnacle Health | $450K | Closed Lost | 3 |

## Key Features

1. **Pre-Call Briefing** — Generated from Hindsight memory
2. **Before/After Toggle** — "With Memory" vs "Without Memory"
3. **Memory Timeline** — What Hindsight recalled from each call
4. **Tactics & Learning** — Cross-deal pattern recognition

## Content Deliverables

- [ ] Article (800-1,500 words) — per team member
- [ ] LinkedIn post — per team member
- [ ] Demo video (2-5 min) — one per team

## GitHub Repo
https://github.com/nayanatara07/deal_intelligence_agent

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `delete_deal_data` import error | Stop Streamlit, delete `src\__pycache__`, restart |
| `UNIQUE constraint failed` | Click "Process with Hindsight" again (auto-cleans old data) |
| `Cannot connect to localhost:8888` | Start Hindsight server first |
| `LLM API key is required` | Set `HINDSIGHT_API_LLM_API_KEY` environment variable |
| SSL/proxy errors with Hindsight Cloud | Use local Hindsight server instead |
| `Remove-Item` not recognized | Use `rmdir /s /q` in cmd, or use PowerShell |
