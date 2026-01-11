# Campaign Brief: Mid-Market Fintech Post-Funding

<!--
This is an EXAMPLE campaign to show how all the pieces fit together.
Use this as a template for your actual campaigns.

THE WORKFLOW:
1. Define campaign (this file)
2. Pull relevant customers and research (pulled_customers.csv, research/)
3. Generate messaging hypotheses (hypotheses/)
4. Create assets (assets/)
5. Execute campaign
6. Track results (results/)
7. Feed learnings back to analysis/ and source/
-->

## Campaign Overview

**Campaign Name**: Mid-Market Fintech Post-Funding
**Start Date**: 2026-01-15
**End Date**: 2026-02-15
**Status**: Planning

**Goal**: Book 10 qualified discovery calls with mid-market fintech companies that raised Series B or C in last 6 months.

---

## Target Definition

### Segment
**From**: `analysis/segmentation/segments.md` - "Mid-Market Fintech"

**Criteria**:
- Industry: Financial Services, Fintech, Digital Banking, Payments
- Headcount: 200-1,000 employees
- Revenue: $10M-$100M ARR
- Geography: North America

### Situational Change
**From**: `analysis/situational_changes/hypotheses.md` - "Post-Funding Round"

**Trigger**: Raised Series B or C in last 6 months

**Why This Works**:
- They have budget ($10M+ raised)
- Board/investors expect faster shipping
- Growth pressure without scaling headcount
- Infrastructure pain becomes acute

**How to Find Them**:
- Crunchbase: Search for Series B/C fintech funding (Q3-Q4 2025)
- LinkedIn: Check for hiring surge (10+ eng roles)
- News: Press releases about growth plans

---

## Target Personas

**Primary**: VP Engineering / CTO (Economic Buyer)
- Has budget authority
- Feels pressure to scale infra
- Prioritizes velocity and reliability

**Secondary**: Engineering Manager (Champion)
- Feels deployment pain daily
- Can advocate internally
- Needs to make boss look good

See `personas.yaml` for messaging per persona.

---

## Hypothesis

**"What Changed" Hypothesis**:
> Mid-market fintech companies that raise Series B/C experience infrastructure pain within 6 months. They go from 15 engineers to 40+, but deployment process is still manual. Board wants faster shipping, but deploys take longer and break more often.

**Evidence**:
- Account_023: "Post-Series B, board wants us 2x faster. Can't keep manually deploying."
- Account_041: "Raised $25M last quarter. Eng team tripled. Deploy process is the bottleneck."
- Account_067: "6 months after funding, we're hiring 20 engineers. Need infra to scale."

**Win Rate**: 45% (vs. 30% baseline) based on past campaigns

---

## Pulled Customers

**From**: `source/crm/derived/accounts_enriched.parquet`

**Query**:
```python
# Filter to mid-market fintech
df = df[(df['industry'].isin(['Fintech', 'Financial Services', 'Digital Banking'])) &
        (df['headcount'] >= 200) &
        (df['headcount'] <= 1000)]

# Check for recent funding (enrichment data)
df = df[df['last_funding_date'] >= '2025-07-01']  # Last 6 months

# Export to campaign folder
df.to_csv('pulled_customers.csv', index=False)
```

**Result**: 47 accounts match criteria (see `pulled_customers.csv`)

**Similar Past Wins** (social proof):
- Account_023: Series B fintech, 350 employees, $50K ARR
- Account_041: Series C digital bank, 650 employees, $48K ARR
- Account_067: Series B payments startup, 280 employees, $35K ARR

---

## Research

**What We Researched** (see `research/` folder):
1. Recent funding announcements (Crunchbase API)
2. Job postings (LinkedIn - are they hiring engineers?)
3. News mentions (Google News - any press about growth?)
4. Tech stack (BuiltWith - are they cloud-native?)

**Key Findings** (see `research/triggers.md`):
- 32 of 47 companies posted DevOps/SRE jobs in last 3 months
- 18 of 47 mentioned "scaling infrastructure" in funding press release
- All 47 are cloud-native (AWS/GCP) - good fit indicator

---

## Messaging Hypotheses

**From**: `hypotheses/messaging_hypotheses.md`

**Hook**: Lead with congratulations on funding + infrastructure pain

**Problem Statement**: "Most fintech teams hit deployment bottleneck 6 months post-raise. Eng team triples but deploy process is still manual."

**Social Proof**: Customer story (Account_023) - similar situation, solved with our product

**Call to Action**: "Worth 15 min to show you how [Customer] scaled post-Series B?"

**Variations**:
1. Email to VP Eng (business outcome focus)
2. Email to Eng Manager (technical pain focus)
3. LinkedIn message (short, conversational)

See `assets/sequences/` for full email copy.

---

## Success Criteria

**Goals**:
- 10 qualified discovery calls booked
- 40%+ email open rate
- 10%+ response rate
- 3+ opportunities created (SQL)

**Measurements** (track in `results/outreach_log.csv`):
- Emails sent: [TBD]
- Opens: [TBD]
- Replies: [TBD]
- Meetings booked: [TBD]
- Opportunities created: [TBD]

---

## Learnings to Capture

**After campaign** (document in `results/learnings.md`):
1. Did "post-funding" messaging resonate?
2. Which persona (VP Eng vs. Eng Manager) responded better?
3. Was timing right (6 months post-funding ideal, or earlier/later)?
4. What objections came up?
5. Did job posting signal correlate with response rate?

**Feed learnings back to**:
- `analysis/situational_changes/hypotheses.md` (refine hypothesis)
- `analysis/segmentation/segments.md` (update segment profile)
- `analysis/win_loss/themes.md` (new win patterns?)

---

## Timeline

- **Week 1**: Research + messaging
- **Week 2-3**: Outreach (3 emails per prospect over 2 weeks)
- **Week 4**: Follow-up + meetings
- **Week 5**: Analysis + learnings doc

---

**Campaign Owner**: _[Name]_
**Last Updated**: 2026-01-15
