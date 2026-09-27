# Deal Intelligence Agent

An AI-powered sales call memory system built with [Hindsight](https://github.com/vectorize-io/hindsight) and [Groq](https://groq.com/).

## What It Does

The Deal Intelligence Agent remembers every call in a deal so a sales rep never walks into call #5 unprepared. It:

- **Ingests** sales call transcripts as they happen
- **Extracts** structured facts (objections, competitors, stakeholders, pricing, tactics)
- **Stores** them in Hindsight's persistent memory
- **Generates** pre-call briefings before every subsequent call
- **Learns** which tactics work across deals

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

- **Hindsight**: Sign up at [ui.hindsight.vectorize.io](https://ui.hindsight.vectorize.io) (use promo code `MEMHACK99` for $50 free credits)
- **Groq**: Sign up at [console.groq.com](https://console.groq.com) (free tier available)

### 3. Start Hindsight (if running locally)

```bash
pip install hindsight-api
export OPENAI_API_KEY=your_key
hindsight-api
```

Or use Hindsight Cloud (no local setup needed).

### 4. Seed the Database

```bash
python seed.py
```

### 5. Run the App

```bash
streamlit run app.py
```

### 6. Process Deals with Hindsight

In the app, click **"Process with Hindsight"** to extract facts from all call transcripts and store them in Hindsight memory.

## Project Structure

```
deal_intelligence_agent/
├── app.py                 # Streamlit UI
├── seed.py                # Database seeding script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
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

## License

MIT
