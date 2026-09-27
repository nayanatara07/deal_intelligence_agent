"""Deal Intelligence Agent - Streamlit UI."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import nest_asyncio
nest_asyncio.apply()

import streamlit as st
from database import (
    init_db, get_all_deals, get_deal, get_calls_for_deal,
    get_objections_for_deal, get_competitors_for_deal,
    get_pricing_for_deal, get_tactics_for_deal, get_stakeholders_for_deal,
    insert_deal, insert_call, insert_objection, insert_competitor,
    insert_pricing, insert_tactic, insert_stakeholder, delete_deal_data
)
from hindsight_layer import HindsightLayer
from extraction import ExtractionPipeline
from briefing import BriefingGenerator
from synthetic_data import get_all_deals as get_synthetic_deals, get_hero_deal

# Page config
st.set_page_config(
    page_title="Deal Intelligence Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
    }
    .memory-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .briefing-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .objection-resolved {
        color: #28a745;
    }
    .objection-unresolved {
        color: #dc3545;
    }
    .tactic-positive {
        color: #28a745;
    }
    .tactic-negative {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_hindsight():
    """Initialize Hindsight layer (cached)."""
    return HindsightLayer()


@st.cache_resource
def get_extraction():
    """Initialize extraction pipeline (cached)."""
    return ExtractionPipeline()


@st.cache_resource
def get_briefing_gen(_hindsight):
    """Initialize briefing generator (cached)."""
    return BriefingGenerator(_hindsight)


def seed_database():
    """Seed the database with synthetic deal data."""
    init_db()

    deals = get_synthetic_deals()

    for deal in deals:
        # Insert deal
        insert_deal(
            deal_id=deal["id"],
            company=deal["company"],
            industry=deal["industry"],
            value=deal["value"],
            stage=deal["stage"],
        )

        # Insert calls
        for call in deal["calls"]:
            call_id = f"{deal['id']}_call_{call['call_number']}"
            insert_call(
                call_id=call_id,
                deal_id=deal["id"],
                call_number=call["call_number"],
                call_date=call["date"],
                transcript=call["transcript"],
            )

    st.success("Database seeded with synthetic deal data!")


def process_deal_with_hindsight(deal_id: str):
    """Process a deal's calls through extraction and Hindsight."""
    hindsight = get_hindsight()
    extraction = get_extraction()

    deal = get_deal(deal_id)
    if not deal:
        st.error(f"Deal {deal_id} not found")
        return

    calls = get_calls_for_deal(deal_id)

    # Delete existing extracted data for clean re-processing
    delete_deal_data(deal_id)

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, call in enumerate(calls):
        status_text.text(f"Processing call {call['call_number']}...")

        # Extract facts
        facts = extraction.extract(
            deal_id=deal_id,
            call_number=call["call_number"],
            company=deal["company"],
            transcript=call["transcript"],
        )

        # Store in database
        for j, obj in enumerate(facts.get("objections", [])):
            insert_objection(
                objection_id=f"{deal_id}_call_{call['call_number']}_obj_{j}",
                call_id=call["id"],
                deal_id=deal_id,
                text=obj["text"],
                raised_by=obj.get("raised_by"),
                resolved=obj.get("resolved", False),
                tactic_used=obj.get("tactic_used"),
            )

        for j, comp in enumerate(facts.get("competitors", [])):
            insert_competitor(
                competitor_id=f"{deal_id}_call_{call['call_number']}_comp_{j}",
                call_id=call["id"],
                deal_id=deal_id,
                name=comp["name"],
                context=comp.get("context"),
                outcome=comp.get("outcome"),
            )

        for j, price in enumerate(facts.get("pricing", [])):
            insert_pricing(
                pricing_id=f"{deal_id}_call_{call['call_number']}_price_{j}",
                call_id=call["id"],
                deal_id=deal_id,
                amount=price.get("amount"),
                discount=price.get("discount"),
                approved=price.get("approved"),
                notes=price.get("notes"),
            )

        for j, tactic in enumerate(facts.get("tactics", [])):
            insert_tactic(
                tactic_id=f"{deal_id}_call_{call['call_number']}_tactic_{j}",
                call_id=call["id"],
                deal_id=deal_id,
                description=tactic["description"],
                outcome=tactic.get("outcome"),
                effectiveness_score=tactic.get("effectiveness_score"),
            )

        for j, stakeholder in enumerate(facts.get("stakeholders", [])):
            insert_stakeholder(
                stakeholder_id=f"{deal_id}_stakeholder_{j}",
                deal_id=deal_id,
                name=stakeholder["name"],
                role=stakeholder.get("role"),
                sentiment=stakeholder.get("sentiment"),
                concerns=stakeholder.get("concerns"),
            )

        # Retain to Hindsight
        hindsight.retain_call(
            deal_id=deal_id,
            call_number=call["call_number"],
            transcript=call["transcript"],
            extracted_facts=facts,
        )

        progress_bar.progress((i + 1) / len(calls))

    status_text.text("Done!")
    st.success(f"Processed {len(calls)} calls for {deal['company']}")


def main():
    """Main Streamlit app."""
    init_db()

    st.markdown('<p class="main-header">Deal Intelligence Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered sales call memory using Hindsight</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Controls")

        if st.button("Seed Database"):
            seed_database()

        st.divider()

        # Deal selection
        deals = get_all_deals()
        if deals:
            deal_options = {f"{d['company']} ({d['id']})": d["id"] for d in deals}
            selected_deal_label = st.selectbox("Select Deal", list(deal_options.keys()))
            selected_deal_id = deal_options[selected_deal_label]
        else:
            st.info("No deals found. Seed the database first.")
            selected_deal_id = None

        st.divider()

        if selected_deal_id:
            if st.button("Process with Hindsight"):
                process_deal_with_hindsight(selected_deal_id)

    # Main content
    if selected_deal_id:
        deal = get_deal(selected_deal_id)
        calls = get_calls_for_deal(selected_deal_id)

        # Deal header
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Company", deal["company"])
        col2.metric("Value", f"${deal['value']:,.0f}")
        col3.metric("Stage", deal["stage"])
        col4.metric("Calls", len(calls))

        st.divider()

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "Pre-Call Briefing",
            "Call Transcripts",
            "Memory Timeline",
            "Tactics & Learning"
        ])

        # Tab 1: Pre-Call Briefing
        with tab1:
            st.header("Pre-Call Briefing")

            if calls:
                next_call = len(calls) + 1
                st.write(f"**Next Call:** Call {next_call}")

                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("Generate Briefing with Memory", type="primary"):
                        with st.spinner("Generating briefing from Hindsight memory..."):
                            hindsight = get_hindsight()
                            briefing_gen = get_briefing_gen(hindsight)
                            briefing = briefing_gen.generate_briefing(
                                deal_id=selected_deal_id,
                                next_call_number=next_call,
                                company=deal["company"],
                            )
                            st.session_state["briefing"] = briefing

                with col2:
                    if st.button("Generate Briefing WITHOUT Memory"):
                        hindsight = get_hindsight()
                        briefing_gen = get_briefing_gen(hindsight)
                        generic = briefing_gen.generate_generic_briefing(
                            deal_id=selected_deal_id,
                            next_call_number=next_call,
                            company=deal["company"],
                        )
                        st.session_state["generic_briefing"] = generic

                # Display briefings side by side
                if "briefing" in st.session_state or "generic_briefing" in st.session_state:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### With Memory")
                        if "briefing" in st.session_state:
                            st.markdown('<div class="briefing-box">', unsafe_allow_html=True)
                            st.write(st.session_state["briefing"]["briefing_text"])
                            st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown("### Without Memory")
                        if "generic_briefing" in st.session_state:
                            st.markdown('<div class="memory-box">', unsafe_allow_html=True)
                            st.write(st.session_state["generic_briefing"])
                            st.markdown('</div>', unsafe_allow_html=True)

        # Tab 2: Call Transcripts
        with tab2:
            st.header("Call Transcripts")

            for call in calls:
                with st.expander(f"Call {call['call_number']} - {call['call_date']}"):
                    st.write(call["transcript"])

        # Tab 3: Memory Timeline
        with tab3:
            st.header("What the Agent Remembers")

            hindsight = get_hindsight()

            # Show recall results for each call
            for call in calls:
                st.subheader(f"Call {call['call_number']} - {call['call_date']}")

                with st.spinner(f"Recalling memories from call {call['call_number']}..."):
                    recall = hindsight.recall_for_briefing(selected_deal_id, call["call_number"])

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Objections**")
                    for obj in recall.get("unresolved_objections", [])[:3]:
                        st.write(f"- {obj}")

                    st.markdown("**Competitors**")
                    for comp in recall.get("competitors", [])[:3]:
                        st.write(f"- {comp}")

                with col2:
                    st.markdown("**Stakeholders**")
                    for stake in recall.get("stakeholders", [])[:3]:
                        st.write(f"- {stake}")

                    st.markdown("**Pricing**")
                    for price in recall.get("pricing", [])[:3]:
                        st.write(f"- {price}")

                st.divider()

        # Tab 4: Tactics & Learning
        with tab4:
            st.header("Tactics & Cross-Deal Learning")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Tactics in This Deal")
                tactics = get_tactics_for_deal(selected_deal_id)
                if tactics:
                    for tactic in tactics:
                        outcome_color = "tactic-positive" if tactic.get("outcome") == "positive" else "tactic-negative"
                        st.markdown(f"- **{tactic['description']}**")
                        st.markdown(f"  Outcome: <span class='{outcome_color}'>{tactic.get('outcome', 'unknown')}</span>", unsafe_allow_html=True)
                        if tactic.get("effectiveness_score"):
                            st.markdown(f"  Effectiveness: {tactic['effectiveness_score']}/5")
                else:
                    st.info("No tactics recorded yet. Process the deal with Hindsight first.")

            with col2:
                st.subheader("Cross-Deal Patterns")
                with st.spinner("Learning from other deals..."):
                    patterns = hindsight.recall_cross_deal_patterns(selected_deal_id)

                if patterns:
                    for pattern in patterns:
                        st.write(f"- {pattern}")
                else:
                    st.info("No cross-deal patterns found. Process more deals first.")

    else:
        st.info("Select a deal from the sidebar to get started.")


if __name__ == "__main__":
    main()
