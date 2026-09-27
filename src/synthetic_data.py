"""Synthetic deal data for the Deal Intelligence Agent."""
import uuid
from datetime import datetime, timedelta

# Hero deal - the one we'll demo live
HERO_DEAL = {
    "id": "deal_nexus_001",
    "company": "Nexus Analytics",
    "industry": "HR Tech",
    "value": 250000,
    "stage": "Negotiation",
    "calls": [
        {
            "call_number": 1,
            "date": "2026-09-01",
            "transcript": """
Sales Rep (SR): Thanks for taking the time today, Priya. Let me start by understanding your current HR infrastructure.

Priya (CTO, Nexus Analytics): We're using a mix of spreadsheets and an old on-premise HRIS. It's painful. We have 500 employees and growing fast.

SR: What's driving the need to change now?

Priya: We just closed a Series B and are scaling to 800 employees next year. Our current system can't handle it. We need something cloud-native.

SR: What's your timeline for making a decision?

Priya: We want to be live by Q1 next year. So we need to decide by end of October.

SR: Who else is involved in this decision?

Priya: Me, our CFO David, and our VP of People Sarah. David cares about ROI, Sarah cares about employee experience.

SR: What budget range are you thinking?

Priya: We've allocated $250K for this project. But that needs to include implementation.

SR: Got it. Let me put together a proposal and we can reconvene next week.

Priya: Sounds good. One more thing - we're also looking at Rippling. I want to be transparent about that.

SR: Thanks for sharing that. How did you hear about Rippling?

Priya: They came in through a cold email. Their pitch was pretty good on the surface.
"""
        },
        {
            "call_number": 2,
            "date": "2026-09-08",
            "transcript": """
SR: Good to see you again, Priya. I've put together a proposal based on our last conversation. Let me walk you through it.

Priya: Go ahead.

SR: Our platform would cost $250K annually for 500 users, with implementation included. That's within your budget.

Priya: That's at the top of our budget. What about the user experience? Sarah was asking about that.

SR: We have a modern, consumer-grade interface. I can set up a demo for Sarah.

Priya: That would be good. But I have to be honest - Rippling quoted us $200K. That's a significant difference.

SR: I understand. Can I ask what specifically they're including for that price?

Priya: Similar features, but their implementation is extra. So it's probably comparable in the end.

SR: That's helpful context. What else is important to you besides price?

Priya: Integration with our existing tech stack. We use Salesforce, Slack, and Workday.

SR: We integrate with all of those natively. Let me show you the integrations in the demo.

Priya: OK. I'm also concerned about data migration. We have 10 years of employee data in our current system.

SR: We have a dedicated migration team. That's included in the implementation.

Priya: Good. Let me discuss with David and Sarah and get back to you.
"""
        },
        {
            "call_number": 3,
            "date": "2026-09-15",
            "transcript": """
SR: Hi Priya, thanks for making time. I wanted to follow up on our last conversation.

Priya: Yes, I talked to David and Sarah. David has some concerns about ROI.

SR: What specifically is he concerned about?

Priya: He wants to see a clear ROI calculation. He's worried that $250K is a lot to spend when we're still growing.

SR: That's fair. Let me put together a detailed ROI analysis. Can I ask - what would success look like for David?

Priya: He wants to see that this will save us money in the long run. We're spending a lot on manual HR processes right now.

SR: How much are you spending on manual processes currently?

Priya: Probably $150K a year in contractor costs and wasted time.

SR: So if we can show that our platform reduces that by 50%, that's $75K in savings. Plus the efficiency gains for your HR team.

Priya: That's the kind of analysis David wants to see. Can you send that over?

SR: Absolutely. I'll have it to you by tomorrow. How's Sarah feeling about the platform?

Priya: She's positive. She liked the demo. Her only concern is adoption - she wants to make sure employees will actually use it.

SR: We have a 95% adoption rate across our customers. I can share case studies.

Priya: That would help. Let me talk to David once I see the ROI analysis.
"""
        },
        {
            "call_number": 4,
            "date": "2026-09-22",
            "transcript": """
SR: Hi Priya, I sent over the ROI analysis yesterday. Did you get a chance to look at it?

Priya: Yes, I did. I showed it to David. He's... cautiously optimistic.

SR: What does that mean?

Priya: He likes the numbers, but he's still concerned about the total cost. He's asking if there's any flexibility on price.

SR: I can talk to my team about that. What number would work for David?

Priya: He mentioned $220K. He feels that's more in line with the market.

SR: I understand. Let me see what I can do. Can I ask - is price the only remaining concern?

Priya: Mostly. Sarah is still a bit worried about the implementation timeline. She wants to make sure we can be live by Q1.

SR: We can definitely do that. Our typical implementation is 6-8 weeks. If we start in November, we'd be live by January.

Priya: That works. But David is also asking about vendor lock-in. He's worried about being stuck with you long-term.

SR: That's a valid concern. We have a 3-year contract with an exit clause after year 2. And we're confident in our platform - our churn rate is under 5%.

Priya: OK. Let me talk to David about the price. I think if you can get closer to $220K, we can move forward.

SR: I'll work on that and get back to you by end of week.
"""
        },
        {
            "call_number": 5,
            "date": "2026-09-29",
            "transcript": """
SR: Hi Priya, I have some good news. My team approved a revised price of $220K for the first year.

Priya: That's great. Let me check with David.

SR: Of course. Also, I wanted to share that we've completed implementations with two other companies in your industry - both went live on schedule.

Priya: That's reassuring. What were their names?

SR: I can't share names due to NDA, but I can share their results. Both saw 40% reduction in HR admin time within 3 months.

Priya: That's impressive. Let me talk to David and get back to you by tomorrow.

SR: Perfect. Looking forward to it.
"""
        }
    ]
}

# Background deals for cross-deal learning
BACKGROUND_DEALS = [
    {
        "id": "deal_vertex_002",
        "company": "Vertex Solutions",
        "industry": "Fintech",
        "value": 180000,
        "stage": "Closed Won",
        "calls": [
            {
                "call_number": 1,
                "date": "2026-08-01",
                "transcript": """
SR: Thanks for your time, Mike. Tell me about your current setup.

Mike (VP Engineering, Vertex Solutions): We're using a legacy system. It's slow and our team hates it.

SR: What's the biggest pain point?

Mike: Speed. Our engineers waste hours every week on manual processes.

SR: How many engineers do you have?

Mike: About 200. We're growing to 300 next year.

SR: What's your budget for this?

Mike: Around $180K. But I need to justify it to our CFO.

SR: What would help you justify it?

Mike: Clear ROI. Show me the time savings.
"""
            },
            {
                "call_number": 2,
                "date": "2026-08-08",
                "transcript": """
SR: Mike, I've put together an ROI analysis based on our last call.

Mike: Let's see it.

SR: Based on 200 engineers saving 5 hours per week, that's 1,000 hours per week. At $75/hour fully loaded, that's $75K per week in savings. Over a year, that's $3.9M in savings.

Mike: That's compelling. But our CFO will ask about the $180K cost vs. the savings.

SR: The ROI is 21x in year one alone. Plus, we're reducing errors and improving compliance.

Mike: I like it. Let me take it to the CFO.

SR: Happy to join that call if it helps.
"""
            },
            {
                "call_number": 3,
                "date": "2026-08-15",
                "transcript": """
SR: Mike, good news?

Mike: The CFO approved it. We're ready to move forward. But she wants a 10% discount.

SR: I can do that. $162K for the first year.

Mike: Perfect. Let's get the paperwork started.
"""
            }
        ]
    },
    {
        "id": "deal_aurora_003",
        "company": "Aurora Retail Group",
        "industry": "Retail",
        "value": 320000,
        "stage": "Closed Won",
        "calls": [
            {
                "call_number": 1,
                "date": "2026-07-01",
                "transcript": """
SR: Thanks for meeting, Jennifer. What's driving this project?

Jennifer (COO, Aurora Retail Group): We're opening 50 new stores next year. Our current system can't scale.

SR: What system are you using now?

Jennifer: An old on-premise solution. It's reliable but not flexible.

SR: What does "not flexible" mean?

Jennifer: We can't customize workflows for different store formats. And reporting is painful.

SR: What's your budget?

Jennifer: $320K. But we need to see clear value.

SR: What does clear value look like?

Jennifer: We need to see that this will reduce our operational costs by at least 20%.
"""
            },
            {
                "call_number": 2,
                "date": "2026-07-08",
                "transcript": """
SR: Jennifer, I've analyzed your operations. Here's what I found.

Jennifer: Go ahead.

SR: You're currently spending $200K per year on manual reporting and reconciliation. Our platform automates 80% of that. That's $160K in savings.

Jennifer: That's good. But what about the implementation? We can't afford downtime.

SR: We do phased rollouts. We'd start with 10 stores, then expand. Zero downtime.

Jennifer: That works. But I'm concerned about our store managers adopting new technology.

SR: We have a dedicated training team. And our UI is designed for non-technical users.

Jennifer: OK. Let me discuss with the CEO.

SR: Happy to present to the CEO if that helps.
"""
            },
            {
                "call_number": 3,
                "date": "2026-07-15",
                "transcript": """
SR: Jennifer, how did it go with the CEO?

Jennifer: She's on board. But she wants to see a pilot first. 10 stores, 3 months.

SR: We can do that. We'll do a pilot at no cost.

Jennifer: Perfect. If the pilot goes well, we'll sign for all 50 stores.

SR: Deal. Let's get the pilot started.
"""
            }
        ]
    },
    {
        "id": "deal_pinnacle_004",
        "company": "Pinnacle Health",
        "industry": "Healthcare",
        "value": 450000,
        "stage": "Closed Lost",
        "calls": [
            {
                "call_number": 1,
                "date": "2026-06-01",
                "transcript": """
SR: Thanks for your time, Dr. Patel. Tell me about your needs.

Dr. Patel (CIO, Pinnacle Health): We need a new patient management system. Our current one is from 2010.

SR: What's wrong with it?

Dr. Patel: It's slow, it's not HIPAA compliant anymore, and it doesn't integrate with our EHR.

SR: What's your budget?

Dr. Patel: $450K. But we have strict compliance requirements.

SR: We're HIPAA compliant and integrate with all major EHRs.

Dr. Patel: Good. But we're also looking at Epic and Cerner.

SR: Those are much more expensive. How much are they quoting?

Dr. Patel: Epic is $800K. Cerner is $600K.

SR: We're significantly cheaper. What else matters to you?

Dr. Patel: Support. We need 24/7 support with a 1-hour response time.
"""
            },
            {
                "call_number": 2,
                "date": "2026-06-08",
                "transcript": """
SR: Dr. Patel, I've checked with our team. We can offer 24/7 support with a 1-hour response time.

Dr. Patel: Good. But I'm still concerned about the implementation timeline. We need to be live by January.

SR: We can do that. Our typical implementation is 12 weeks.

Dr. Patel: That's cutting it close. What if there are delays?

SR: We have a dedicated implementation manager. And we offer a service level agreement with penalties for delays.

Dr. Patel: OK. Let me discuss with our board.

SR: Happy to present to the board.
"""
            },
            {
                "call_number": 3,
                "date": "2026-06-15",
                "transcript": """
SR: Dr. Patel, any updates?

Dr. Patel: I'm sorry, we went with Epic.

SR: Can I ask why?

Dr. Patel: The board felt more comfortable with a larger vendor. It was a risk mitigation decision, not a product decision.

SR: I understand. If anything changes, please reach out.

Dr. Patel: Of course. You were very responsive throughout the process.
"""
            }
        ]
    }
]


def get_all_deals():
    """Get all deals (hero + background)."""
    return [HERO_DEAL] + BACKGROUND_DEALS


def get_hero_deal():
    """Get the hero deal for demo."""
    return HERO_DEAL


def get_deal_by_id(deal_id):
    """Get a deal by ID."""
    for deal in get_all_deals():
        if deal["id"] == deal_id:
            return deal
    return None
