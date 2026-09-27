"""Configuration management for the Deal Intelligence Agent."""
import os
from dotenv import load_dotenv

load_dotenv()

# Hindsight configuration
# For Hindsight Cloud, use: https://api.hindsight.vectorize.io
# For local server, use: http://localhost:8888
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "deal-intelligence")

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Set Hindsight's internal LLM env vars from Groq config
# This allows `hindsight-api` to use Groq without manual env var setup
os.environ["HINDSIGHT_API_LLM_API_KEY"] = GROQ_API_KEY
os.environ["HINDSIGHT_API_LLM_BASE_URL"] = "https://api.groq.com/openai/v1"
os.environ["HINDSIGHT_API_LLM_MODEL"] = GROQ_MODEL

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/deals.db")

# Hindsight bank mission and directives
HINDSIGHT_MISSION = (
    "You are a sales deal intelligence agent. You track objections, competitors, "
    "stakeholder concerns, and pricing across the entire deal cycle. You brief "
    "sales reps before calls and learn which tactics work best."
)

HINDSIGHT_DIRECTIVES = [
    "Always track who raised an objection and what it was",
    "Track competitor mentions and how they were handled",
    "Record pricing discussions and concessions made",
    "Note which tactics led to positive outcomes",
    "Track stakeholder sentiment changes across calls",
    "When recalling, prioritize recent information but surface unresolved older items",
]
