"""Pre-call briefing generator using Hindsight memory."""
import logging
from hindsight_layer import HindsightLayer

logger = logging.getLogger(__name__)


class BriefingGenerator:
    """Generates pre-call briefings using Hindsight recall and reflect."""

    def __init__(self, hindsight_layer: HindsightLayer):
        self.hindsight = hindsight_layer

    def generate_briefing(self, deal_id: str, next_call_number: int, company: str) -> dict:
        """Generate a pre-call briefing using Hindsight memory."""
        # Recall all relevant memories
        recall_results = self.hindsight.recall_for_briefing(deal_id, next_call_number)

        # Generate natural language briefing using reflect
        briefing_text = self.hindsight.reflect_briefing(deal_id, next_call_number)

        # Get cross-deal patterns (stretch feature)
        cross_deal_patterns = self.hindsight.recall_cross_deal_patterns(deal_id)

        return {
            "deal_id": deal_id,
            "company": company,
            "next_call_number": next_call_number,
            "briefing_text": briefing_text,
            "recall_results": recall_results,
            "cross_deal_patterns": cross_deal_patterns,
        }

    def generate_generic_briefing(self, deal_id: str, next_call_number: int, company: str) -> str:
        """Generate a generic briefing without memory (for before/after comparison)."""
        return f"""Generic Pre-Call Briefing for {company} - Call {next_call_number}

This is what you'd get WITHOUT memory:

• Review your CRM notes before the call
• Remember to ask about budget and timeline
• Be prepared to discuss pricing
• Ask about decision-making process
• Follow up on any previous commitments

Tip: Without memory, every call starts from zero. You rely on the rep's
memory and scattered notes to piece together the deal context."""

    def format_briefing_for_display(self, briefing: dict) -> str:
        """Format the briefing for display in the UI."""
        lines = [
            f"# Pre-Call Briefing: {briefing['company']}",
            f"**Call {briefing['next_call_number']}**",
            "",
            briefing["briefing_text"],
            "",
            "---",
            "## What the Agent Remembers",
        ]

        # Add recall results
        for key, memories in briefing.get("recall_results", {}).items():
            if memories:
                lines.append(f"\n### {key.replace('_', ' ').title()}")
                for memory in memories[:3]:  # Limit to 3 per category
                    lines.append(f"- {memory}")

        # Add cross-deal patterns
        patterns = briefing.get("cross_deal_patterns", [])
        if patterns:
            lines.append("\n---")
            lines.append("## Cross-Deal Learning")
            lines.append("Patterns from other deals:")
            for pattern in patterns[:3]:
                lines.append(f"- {pattern}")

        return "\n".join(lines)
