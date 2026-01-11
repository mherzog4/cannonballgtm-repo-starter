# Market Segmentation

<!--
PURPOSE: Document your customer segments based on how people buy and the problems they have.
This is where you identify patterns in your best customers.

THE WORKFLOW:
1. Load your CRM data with ARR and enrichment (industry, headcount)
2. Match with transcripts to understand problem sets
3. Ask: "Who's doing really well? What patterns do I see?"
4. Segment by industry, headcount, and how they buy
5. Create hypotheses about what makes each segment successful
6. Test these hypotheses in campaigns and iterate

WHY THIS MATTERS:
Different segments buy differently and have different problems.
Mid-market fintech cares about compliance. Enterprise cares about integration.
If you message everyone the same way, you're not speaking to anyone specifically.

HOW TO USE:
- Reference when planning campaigns
- Update after each campaign with learnings
- Use segment definitions in pipelines/segment.py to auto-classify accounts
-->

## Segment Definition Framework

For each segment, document:
1. **Who they are** (firmographics: industry, headcount, revenue)
2. **How they buy** (sales cycle, buying committee, deal size)
3. **What problems they have** (pain points, use cases)
4. **What makes them win** (why they chose you)
5. **Evidence** (citations from transcripts, deal data)

---

## Example Segment: Mid-Market Fintech

<!-- Replace this example with your actual segments -->

### Who They Are

**Firmographics**:
- Industry: Financial Services (focus: Fintech, Digital Banking)
- Headcount: 200 to 1,000 employees
- Revenue: $10M to $100M ARR
- Geography: North America, UK
- Funding Stage: Series B to Series D

**Tech Stack Indicators**:
- Using AWS or GCP (cloud-native)
- Modern stack (React, Node.js, Python)
- Already using CI/CD tools (GitHub Actions, CircleCI)

### How They Buy

**Sales Cycle**: 4-8 weeks
**Average Deal Size**: $30K to $60K first year

**Buying Committee**:
- Champion: Engineering Manager or Senior Engineer
- Economic Buyer: VP Engineering or CTO
- Technical Buyer: Security team (often involved due to compliance)

**Decision Criteria**:
1. Compliance/security (SOC 2, GDPR)
2. Time to value (need to deploy fast)
3. Scalability (growing quickly)

### What Problems They Have

**Primary Pain Point**: Manual deployment processes that don't scale

**Why This Hurts Them**:
- Shipping features is slow (weeks, not days)
- Risk-averse because deploy failures are costly
- Small eng team (10-30 engineers), can't dedicate someone to DevOps full-time

**What They've Tried**:
- Jenkins + homegrown scripts (brittle, doesn't scale)
- GitHub Actions (works for CI, not CD)
- Considered Datadog but it's expensive and doesn't solve deployment

**Quote from Champion** (deal won):
> "We were spending 10 hours a week just babysitting deployments. Every deploy felt like a roll of the dice. We needed something that would just work without needing a dedicated DevOps team."
>
> _— Senior Engineer at Account_023 (Fintech, 350 employees, $50K ARR)_

### What Makes Them Win

**Win Rate**: 45% (vs. 30% overall)

**Why They Choose Us**:
1. **Speed** - Get up and running in 1 day, not 2 weeks
2. **No DevOps team needed** - Eng team can self-serve
3. **Compliance built-in** - Audit logs, SOC 2 compliant
4. **Pricing model** - Per-project, not per-seat (aligns with their usage)

**Common Objections** (and how we handle them):
- "We're building our own" → _"You're Series B, focus on your product, not internal tools"_
- "Seems expensive" → _"Cost of one outage > annual platform cost. Think of it as insurance."_

**Lose To**:
- Building in-house (30% of lost deals)
- Deciding to stick with Jenkins (20% of lost deals)

### Evidence & Citations

**Transcript Citations**:
- See `source/transcripts/normalized/` calls with Account_023, Account_041, Account_067
- Search for: "manual deploy", "DevOps", "compliance", "SOC 2"

**Win Rate Data**:
```sql
-- Query to verify segment win rate
SELECT
    COUNT(DISTINCT o.opportunity_id) as total_deals,
    SUM(CASE WHEN o.is_won THEN 1 ELSE 0 END) as won_deals,
    ROUND(AVG(CASE WHEN o.is_won THEN 1.0 ELSE 0.0 END) * 100, 2) as win_rate
FROM opportunities o
JOIN accounts a ON o.account_id = a.account_id
WHERE a.industry = 'Financial Services'
  AND a.headcount BETWEEN 200 AND 1000
  AND o.is_closed = true
```

**Sample Accounts in This Segment**:
- Account_023: Series B fintech, 350 employees, $50K ARR (won)
- Account_041: Series C digital bank, 650 employees, $48K ARR (won)
- Account_067: Series B payments startup, 280 employees, $35K ARR (won)
- Account_089: Series B lending platform, 420 employees, lost to "building in-house"

---

## Example Segment: SMB SaaS

<!-- Add your own segments below -->

### Who They Are

**Firmographics**:
- Industry: SaaS (horizontal or vertical)
- Headcount: 10 to 100 employees
- Revenue: $1M to $10M ARR
- Funding Stage: Seed to Series A

### How They Buy

**Sales Cycle**: 2-4 weeks
**Average Deal Size**: $10K to $20K first year

**Buying Committee**:
- Often just one person (CTO or Founding Engineer)
- Self-serve motion (trial before buying)

### What Problems They Have

_[Fill in based on your data]_

### What Makes Them Win

_[Fill in based on your data]_

### Evidence & Citations

_[Add citations from transcripts and deal data]_

---

## Segment Comparison

| Segment | Win Rate | Avg Deal Size | Sales Cycle | Top Pain Point |
|---------|----------|---------------|-------------|----------------|
| Mid-Market Fintech | 45% | $45K | 6 weeks | Manual deploys don't scale |
| SMB SaaS | 35% | $15K | 3 weeks | Need something simple and fast |
| _[Add more]_ | | | | |

---

## How to Use Segments in Campaigns

1. **Pick one segment per campaign** - Don't try to message everyone at once
2. **Pull customers in this segment** - `campaigns/*/pulled_customers.csv`
3. **Research situational changes** - What's happening in this segment right now?
4. **Tailor messaging** - Speak directly to their pain points
5. **Measure results** - Did this segment respond better?
6. **Feed learnings back** - Update this file with what worked

See `campaigns/*/` for examples of segment-specific campaigns.

---

## Updating Segments

**When to update**:
- After completing a campaign (what did you learn?)
- Quarterly, based on closed deals analysis
- When entering new market segments

**The compound learning loop**:
1. Analyze source data → Create segment hypotheses
2. Test in campaign → Measure results
3. Feed learnings back → Update this file
4. Next campaign starts smarter → Repeat

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
**Change Log**: _[What changed and why]_
