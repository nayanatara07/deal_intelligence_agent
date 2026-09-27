"""Seed the database with synthetic deal data and process through Hindsight."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from database import init_db, insert_deal, insert_call
from synthetic_data import get_all_deals
from hindsight_layer import HindsightLayer
from extraction import ExtractionPipeline


def seed():
    """Seed the database and process all deals through Hindsight."""
    print("Initializing database...")
    init_db()

    deals = get_all_deals()
    print(f"Found {len(deals)} deals to seed")

    # Insert deals and calls
    for deal in deals:
        print(f"\nSeeding deal: {deal['company']} ({deal['id']})")

        insert_deal(
            deal_id=deal["id"],
            company=deal["company"],
            industry=deal["industry"],
            value=deal["value"],
            stage=deal["stage"],
        )

        for call in deal["calls"]:
            call_id = f"{deal['id']}_call_{call['call_number']}"
            insert_call(
                call_id=call_id,
                deal_id=deal["id"],
                call_number=call["call_number"],
                call_date=call["date"],
                transcript=call["transcript"],
            )
            print(f"  Inserted call {call['call_number']}")

    print("\nDatabase seeded successfully!")
    print("\nNow run the Streamlit app and click 'Process with Hindsight' to extract and store memories.")
    print("Or run: python -c \"from seed import process_all; process_all()\"")


def process_all():
    """Process all deals through extraction and Hindsight."""
    from database import get_all_deals as get_db_deals, get_calls_for_deal
    from database import insert_objection, insert_competitor, insert_pricing, insert_tactic, insert_stakeholder

    print("Initializing Hindsight and extraction pipeline...")
    hindsight = HindsightLayer()
    extraction = ExtractionPipeline()

    deals = get_db_deals()
    print(f"Processing {len(deals)} deals...")

    for deal in deals:
        print(f"\nProcessing deal: {deal['company']} ({deal['id']})")
        calls = get_calls_for_deal(deal["id"])

        for call in calls:
            print(f"  Processing call {call['call_number']}...")

            # Extract facts
            facts = extraction.extract(
                deal_id=deal["id"],
                call_number=call["call_number"],
                company=deal["company"],
                transcript=call["transcript"],
            )

            # Store in database
            for j, obj in enumerate(facts.get("objections", [])):
                insert_objection(
                    objection_id=f"{deal['id']}_call_{call['call_number']}_obj_{j}",
                    call_id=call["id"],
                    deal_id=deal["id"],
                    text=obj["text"],
                    raised_by=obj.get("raised_by"),
                    resolved=obj.get("resolved", False),
                    tactic_used=obj.get("tactic_used"),
                )

            for j, comp in enumerate(facts.get("competitors", [])):
                insert_competitor(
                    competitor_id=f"{deal['id']}_call_{call['call_number']}_comp_{j}",
                    call_id=call["id"],
                    deal_id=deal["id"],
                    name=comp["name"],
                    context=comp.get("context"),
                    outcome=comp.get("outcome"),
                )

            for j, price in enumerate(facts.get("pricing", [])):
                insert_pricing(
                    pricing_id=f"{deal['id']}_call_{call['call_number']}_price_{j}",
                    call_id=call["id"],
                    deal_id=deal["id"],
                    amount=price.get("amount"),
                    discount=price.get("discount"),
                    approved=price.get("approved"),
                    notes=price.get("notes"),
                )

            for j, tactic in enumerate(facts.get("tactics", [])):
                insert_tactic(
                    tactic_id=f"{deal['id']}_call_{call['call_number']}_tactic_{j}",
                    call_id=call["id"],
                    deal_id=deal["id"],
                    description=tactic["description"],
                    outcome=tactic.get("outcome"),
                    effectiveness_score=tactic.get("effectiveness_score"),
                )

            for j, stakeholder in enumerate(facts.get("stakeholders", [])):
                insert_stakeholder(
                    stakeholder_id=f"{deal['id']}_stakeholder_{j}",
                    deal_id=deal["id"],
                    name=stakeholder["name"],
                    role=stakeholder.get("role"),
                    sentiment=stakeholder.get("sentiment"),
                    concerns=stakeholder.get("concerns"),
                )

            # Retain to Hindsight
            hindsight.retain_call(
                deal_id=deal["id"],
                call_number=call["call_number"],
                transcript=call["transcript"],
                extracted_facts=facts,
            )

            print(f"    Extracted: {len(facts.get('objections', []))} objections, "
                  f"{len(facts.get('competitors', []))} competitors, "
                  f"{len(facts.get('tactics', []))} tactics")

    print("\nAll deals processed successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "process":
        process_all()
    else:
        seed()
