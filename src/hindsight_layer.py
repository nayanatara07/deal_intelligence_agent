"""Hindsight memory integration layer."""
import asyncio
import json
import logging
from typing import Optional
from hindsight_client import Hindsight
from config import HINDSIGHT_API_KEY, HINDSIGHT_BASE_URL, HINDSIGHT_BANK_ID, HINDSIGHT_MISSION, HINDSIGHT_DIRECTIVES

logger = logging.getLogger(__name__)

# Single persistent event loop for all async Hindsight operations
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)


class HindsightLayer:
    """Wrapper around the Hindsight client for deal intelligence operations."""

    def __init__(self):
        self.client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY if HINDSIGHT_API_KEY else None,
            timeout=60.0,
        )
        self.bank_id = HINDSIGHT_BANK_ID
        self._ensure_bank_exists()

    def _ensure_bank_exists(self):
        """Create the memory bank if it doesn't exist."""
        try:
            _loop.run_until_complete(self.client.acreate_bank(
                bank_id=self.bank_id,
                name="Deal Intelligence",
                mission=HINDSIGHT_MISSION,
                disposition={
                    "skepticism": 3,
                    "literalism": 3,
                    "empathy": 4,
                },
            ))
            logger.info(f"Created Hindsight bank: {self.bank_id}")
        except Exception as e:
            # Bank likely already exists
            logger.info(f"Bank {self.bank_id} already exists or error: {e}")

    def retain_call(self, deal_id: str, call_number: int, transcript: str, extracted_facts: dict):
        """Retain a call transcript and its extracted facts to Hindsight."""
        # Retain the full transcript
        _loop.run_until_complete(self.client.aretain(
            bank_id=self.bank_id,
            content=transcript,
            context=f"Deal {deal_id} - Call {call_number} transcript",
            document_id=f"{deal_id}_call_{call_number}",
            metadata={
                "deal_id": str(deal_id),
                "call_number": str(call_number),
                "type": "transcript",
            },
        ))

        # Retain each extracted fact as a separate memory
        # This makes retrieval much more precise
        for objection in extracted_facts.get("objections", []):
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Objection in deal {deal_id}, call {call_number}: {objection['text']}. Raised by: {objection.get('raised_by', 'unknown')}. Resolved: {objection.get('resolved', False)}. Tactic used: {objection.get('tactic_used', 'none')}",
                context=f"Deal {deal_id} - Call {call_number} - Objection",
                document_id=f"{deal_id}_call_{call_number}_objection",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "objection",
                    "raised_by": str(objection.get("raised_by", "")),
                    "resolved": str(objection.get("resolved", False)),
                },
            ))

        for competitor in extracted_facts.get("competitors", []):
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Competitor mentioned in deal {deal_id}, call {call_number}: {competitor['name']}. Context: {competitor.get('context', '')}. Outcome: {competitor.get('outcome', '')}",
                context=f"Deal {deal_id} - Call {call_number} - Competitor",
                document_id=f"{deal_id}_call_{call_number}_competitor",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "competitor",
                    "name": str(competitor["name"]),
                },
            ))

        for stakeholder in extracted_facts.get("stakeholders", []):
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Stakeholder in deal {deal_id}: {stakeholder['name']}, role: {stakeholder.get('role', 'unknown')}. Sentiment in call {call_number}: {stakeholder.get('sentiment', 'neutral')}. Concerns: {stakeholder.get('concerns', '')}",
                context=f"Deal {deal_id} - Call {call_number} - Stakeholder",
                document_id=f"{deal_id}_call_{call_number}_stakeholder",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "stakeholder",
                    "name": str(stakeholder["name"]),
                    "sentiment": str(stakeholder.get("sentiment", "neutral")),
                },
            ))

        for pricing in extracted_facts.get("pricing", []):
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Pricing discussion in deal {deal_id}, call {call_number}: amount=${pricing.get('amount', 'unknown')}, discount={pricing.get('discount', 'none')}, approved={pricing.get('approved', 'unknown')}. Notes: {pricing.get('notes', '')}",
                context=f"Deal {deal_id} - Call {call_number} - Pricing",
                document_id=f"{deal_id}_call_{call_number}_pricing",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "pricing",
                    "amount": str(pricing.get("amount", "")),
                },
            ))

        for tactic in extracted_facts.get("tactics", []):
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Tactic used in deal {deal_id}, call {call_number}: {tactic['description']}. Outcome: {tactic.get('outcome', 'unknown')}. Effectiveness: {tactic.get('effectiveness_score', 'unknown')}/5",
                context=f"Deal {deal_id} - Call {call_number} - Tactic",
                document_id=f"{deal_id}_call_{call_number}_tactic",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "tactic",
                    "outcome": str(tactic.get("outcome", "")),
                    "effectiveness_score": str(tactic.get("effectiveness_score", "")),
                },
            ))

        # Retain a summary of the call
        summary = extracted_facts.get("summary", "")
        if summary:
            _loop.run_until_complete(self.client.aretain(
                bank_id=self.bank_id,
                content=f"Summary of deal {deal_id}, call {call_number}: {summary}",
                context=f"Deal {deal_id} - Call {call_number} - Summary",
                document_id=f"{deal_id}_call_{call_number}_summary",
                metadata={
                    "deal_id": str(deal_id),
                    "call_number": str(call_number),
                    "type": "summary",
                },
            ))

        logger.info(f"Retained call {call_number} for deal {deal_id} to Hindsight")

    def recall_for_briefing(self, deal_id: str, next_call_number: int) -> dict:
        """Recall all relevant memories for generating a pre-call brief."""
        # Query for different aspects of the deal
        queries = {
            "overall_deal": f"What is the current state of deal {deal_id}? What stage is it in?",
            "unresolved_objections": f"What objections have been raised in deal {deal_id} that are still unresolved?",
            "competitors": f"What competitors have been mentioned in deal {deal_id} and how were they handled?",
            "pricing": f"What pricing discussions have happened in deal {deal_id}? What was the last price discussed?",
            "stakeholders": f"Who are the key stakeholders in deal {deal_id} and what are their current concerns and sentiment?",
            "commitments": f"What commitments or follow-ups were made in deal {deal_id}?",
            "successful_tactics": f"What tactics have worked well in deal {deal_id}?",
        }

        results = {}
        for key, query in queries.items():
            try:
                response = _loop.run_until_complete(self.client.arecall(
                    bank_id=self.bank_id,
                    query=query,
                    max_tokens=2048,
                    budget="mid",
                ))
                results[key] = [r.text for r in response.results]
            except Exception as e:
                logger.error(f"Error recalling {key} for deal {deal_id}: {e}")
                results[key] = []

        return results

    def reflect_briefing(self, deal_id: str, next_call_number: int, context: str = "") -> str:
        """Use Hindsight reflect to generate a natural language briefing."""
        query = f"Generate a pre-call briefing for call {next_call_number} of deal {deal_id}. Include: current deal state, unresolved objections, competitor landscape, pricing context, stakeholder sentiment, and suggested talking points. Be specific and concise."
        if context:
            query += f" Additional context: {context}"

        try:
            response = _loop.run_until_complete(self.client.areflect(
                bank_id=self.bank_id,
                query=query,
                budget="high",
                context=f"Preparing for call {next_call_number} of deal {deal_id}",
            ))
            return response.text
        except Exception as e:
            logger.error(f"Error generating briefing for deal {deal_id}: {e}")
            return f"Error generating briefing: {e}"

    def recall_cross_deal_patterns(self, current_deal_id: str) -> list:
        """Recall patterns from other deals for cross-deal learning."""
        try:
            response = _loop.run_until_complete(self.client.arecall(
                bank_id=self.bank_id,
                query=f"What objection-handling tactics have been successful in other deals? What patterns do you see across deals?",
                max_tokens=2048,
                budget="mid",
            ))
            return [r.text for r in response.results]
        except Exception as e:
            logger.error(f"Error recalling cross-deal patterns: {e}")
            return []
