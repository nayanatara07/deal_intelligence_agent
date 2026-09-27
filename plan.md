# Deal Intelligence Agent — Hackathon Plan

## One-Liner
**"An AI that remembers every call in a deal so a rep never walks into call #5 unprepared."**

## Tech Stack
- **Memory**: Hindsight Cloud (Vectorize) — `https://api.hindsight.vectorize.io`
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

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env`:**
   ```env
   HINDSIGHT_API_KEY=your_hindsight_api_key
   HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
   GROQ_API_KEY=your_groq_api_key
   ```

3. **Seed database:**
   ```bash
   python seed.py
   ```

4. **Run app:**
   ```bash
   streamlit run app.py
   ```

5. **In the app:**
   - Click "Seed Database"
   - Select a deal (e.g., Acme Corp)
   - Click "Process with Hindsight"
   - Go to "Pre-Call Briefing" tab
   - Click "Generate Briefing with Memory"

## Demo Flow (60-90 seconds)

1. **Set the scene (10s):** "You're an AE. You've had 4 calls with Acme Corp — a $250K HR software deal. It's 5 minutes before call 5."

2. **Show the brief (20s):** Click "Generate Briefing with Memory" — surface a specific remembered detail (e.g., "Priya raised a security concern in call 2 that was never followed up on").

3. **Show it acting on memory (20s):** Ask the agent a question mid-"call" and show it answering from accumulated memory.

4. **Show the learning curve (20s):** Show cross-deal patterns — "The ROI calculator tactic worked in 3 other deals, use it again."

5. **Close (10s):** "Without memory, every call starts from zero. With memory, reps save 2-3 hours per week on prep."

## Synthetic Data

| Deal | Company | Value | Stage | Calls |
|------|---------|-------|-------|-------|
| Hero | Acme Corp | $250K | Negotiation | 5 |
| Background | TechCorp | $180K | Closed Won | 3 |
| Background | RetailMax | $320K | Closed Won | 3 |
| Background | HealthFirst | $450K | Closed Lost | 3 |

## Key Features

1. **Pre-Call Briefing** — Generated from Hindsight memory
2. **Before/After Toggle** — "With Memory" vs "Without Memory"
3. **Memory Timeline** — What Hindsight recalled from each call
4. **Tactics & Learning** — Cross-deal pattern recognition

## Content Deliverables

- [ ] Article (800-1,500 words) — per team member
- [ ] LinkedIn post — per team member
- [ ] Demo video (2-5 min) — one per team

## GitHub Setup

```bash
cd C:\Users\USER\source\repos\deal_intelligence_agent
git init
git add .
git commit -m "Deal Intelligence Agent - Hindsight memory for sales calls"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/deal_intelligence_agent.git
git push -u origin main
```

## Timeline

| Phase | Time | Status |
|-------|------|--------|
| Setup | Hr 0-2 | Done |
| Data | Hr 2-5 | Done |
| Core pipeline | Hr 5-14 | Done |
| UI | Hr 14-18 | Done |
| Cross-deal learning | Hr 18-24 | Done |
| Polish + demo | Hr 24-30 | In Progress |
| Content deliverables | Hr 30+ | Pending |
