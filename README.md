# Deal Intelligence Agent

An AI-powered sales call memory system built with [Hindsight](https://github.com/vectorize-io/hindsight) and [Groq](https://groq.com/).

## What It Does

The Deal Intelligence Agent remembers every call in a deal so a sales rep never walks into call #5 unprepared. It:

- **Ingests** sales call transcripts as they happen
- **Extracts** structured facts (objections, competitors, stakeholders, pricing, tactics)
- **Stores** them in Hindsight's persistent memory
- **Generates** pre-call briefings before every subsequent call
- **Learns** which tactics work across deals

## Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com) (free tier, no credit card)
- [Hindsight API key](https://ui.hindsight.vectorize.io) (use promo code `MEMHACK99` for $50 free credits)

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/nayanatara07/deal_intelligence_agent.git
cd deal_intelligence_agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install hindsight-api
```

### 2. Configure `.env`

Copy `.env.example` to `.env` and fill in your keys:

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

### 3. Start Hindsight Server (Terminal 1)

Create a file called `start-hindsight.bat` in the project folder:

```bat
@echo off
set HINDSIGHT_API_LLM_API_KEY=your_groq_api_key
set HINDSIGHT_API_LLM_BASE_URL=https://api.groq.com/openai/v1
set HINDSIGHT_API_LLM_MODEL=openai/gpt-oss-120b
hindsight-api
```

Or run these commands directly in cmd.exe:

```cmd
set HINDSIGHT_API_LLM_API_KEY=your_groq_api_key
set HINDSIGHT_API_LLM_BASE_URL=https://api.groq.com/openai/v1
set HINDSIGHT_API_LLM_MODEL=openai/gpt-oss-120b
hindsight-api
```

### 4. Run the App (Terminal 2)

```cmd
streamlit run app.py
```

### 5. Use the App

1. Click **"Seed Database"** in the sidebar
2. Select **"Nexus Analytics"** from the dropdown
3. Click **"Process with Hindsight"** — extracts facts from all calls and stores in memory
4. Go to **"Pre-Call Briefing"** tab
5. Click **"Generate Briefing with Memory"** — see what the agent remembers
6. Click **"Generate Briefing WITHOUT Memory"** — compare with generic advice

> **Note:** Both terminals must be running at the same time. The Hindsight server provides the memory layer, and Streamlit provides the UI.

## Project Structure

```
deal_intelligence_agent/
├── app.py                 # Streamlit UI
├── seed.py                # Database seeding script
├── start-hindsight.bat    # Hindsight server launcher
├── requirements.txt       # Python dependencies
├── .env / .env.example    # Environment template
├── README.md              # This file
├── plan.md                # Full project plan
├── data/
│   └── deals.db           # SQLite database
└── src/
    ├── config.py          # Configuration
    ├── database.py        # SQLite models
    ├── hindsight_layer.py # Hindsight integration
    ├── extraction.py      # LLM extraction pipeline
    ├── briefing.py        # Briefing generator
    └── synthetic_data.py  # Synthetic deal data
```

## How It Works

1. **Ingestion**: Sales call transcripts are fed into the system
2. **Extraction**: An LLM (Groq) extracts structured facts — objections, competitors, stakeholders, pricing, tactics
3. **Memory**: Facts are stored in Hindsight as discrete, searchable memories
4. **Recall**: Before the next call, Hindsight recalls all relevant memories
5. **Briefing**: An LLM generates a natural-language pre-call briefing
6. **Learning**: Cross-deal patterns are surfaced as tactical suggestions

## Tech Stack

- **Memory**: [Hindsight](https://hindsight.vectorize.io/) by Vectorize
- **LLM**: [Groq](https://groq.com/) (gpt-oss-120b)
- **UI**: [Streamlit](https://streamlit.io/)
- **Database**: SQLite

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cannot connect to localhost:8888` | Start Hindsight server in Terminal 1 |
| `LLM API key is required` | Set `HINDSIGHT_API_LLM_API_KEY` in Terminal 1 |
| `model gpt-4o-mini does not exist` | Set `HINDSIGHT_API_LLM_MODEL=openai/gpt-oss-120b` in Terminal 1 |
| `UNIQUE constraint failed` | Fixed — all inserts use `INSERT OR REPLACE` |
| `Event loop is closed` | Fixed — using persistent event loop |
| `Timeout context manager` | Fixed — using `asyncio.run()` for all Hindsight calls |

## License

MIT
