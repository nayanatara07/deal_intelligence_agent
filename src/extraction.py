"""LLM-based extraction pipeline for sales call transcripts."""
import json
import logging
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = (
    "You are a sales call analyzer. Extract structured facts from the following sales call transcript.\n\n"
    "Return ONLY valid JSON with this exact structure:\n"
    "{\n"
    '  "summary": "One sentence summary of the call",\n'
    '  "objections": [\n'
    '    {"text": "the objection", "raised_by": "name", "resolved": true/false, "tactic_used": "tactic name or null"}\n'
    "  ],\n"
    '  "competitors": [\n'
    '    {"name": "competitor name", "context": "how they were mentioned", "outcome": "how it was handled"}\n'
    "  ],\n"
    '  "stakeholders": [\n'
    '    {"name": "name", "role": "role", "sentiment": "positive/neutral/negative", "concerns": "their concerns"}\n'
    "  ],\n"
    '  "pricing": [\n'
    '    {"amount": 123456, "discount": "10%", "approved": true/false, "notes": "context"}\n'
    "  ],\n"
    '  "tactics": [\n'
    '    {"description": "tactic used", "outcome": "result", "effectiveness_score": 1-5}\n'
    "  ],\n"
    '  "commitments": ["commitment 1", "commitment 2"]\n'
    "}\n\n"
    "Deal: {deal_id}\n"
    "Call: {call_number}\n"
    "Company: {company}\n\n"
    "Transcript:\n"
    "{transcript}\n\n"
    "Return ONLY the JSON, no other text."
)


class ExtractionPipeline:
    """Extracts structured facts from sales call transcripts using Groq."""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def extract(self, deal_id: str, call_number: int, company: str, transcript: str) -> dict:
        """Extract structured facts from a call transcript."""
        prompt = (
            EXTRACTION_PROMPT
            + f"\n\nDeal: {deal_id}\n"
            + f"Call: {call_number}\n"
            + f"Company: {company}\n\n"
            + f"Transcript:\n{transcript}\n\n"
            + "Return ONLY the JSON, no other text."
        )

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a precise sales call analyzer. Return only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                    max_tokens=4096,
                )

                text = response.choices[0].message.content.strip()

                # Try to extract JSON from the response
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]

                result = json.loads(text)

                # Validate structure
                result.setdefault("summary", "")
                result.setdefault("objections", [])
                result.setdefault("competitors", [])
                result.setdefault("stakeholders", [])
                result.setdefault("pricing", [])
                result.setdefault("tactics", [])
                result.setdefault("commitments", [])

                logger.info(f"Extracted facts from call {call_number} of deal {deal_id}")
                return result

            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error on attempt {attempt + 1}: {e}")
                if attempt == 2:
                    # Return empty structure on final failure
                    return {
                        "summary": "",
                        "objections": [],
                        "competitors": [],
                        "stakeholders": [],
                        "pricing": [],
                        "tactics": [],
                        "commitments": [],
                    }
            except Exception as e:
                logger.error(f"Extraction error on attempt {attempt + 1}: {e}")
                if attempt == 2:
                    return {
                        "summary": "",
                        "objections": [],
                        "competitors": [],
                        "stakeholders": [],
                        "pricing": [],
                        "tactics": [],
                        "commitments": [],
                    }

        return {
            "summary": "",
            "objections": [],
            "competitors": [],
            "stakeholders": [],
            "pricing": [],
            "tactics": [],
            "commitments": [],
        }
