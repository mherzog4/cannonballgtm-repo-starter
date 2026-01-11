# Situational Change Hypotheses

<!--
PURPOSE: Document what changed in prospects' businesses that made them need you NOW.
This is your "why now" - the trigger events that create buying windows.

THE WORKFLOW:
1. For each segment, read transcripts from won deals
2. Look for what changed: funding, new hire, outage, growth pain, compliance deadline
3. Create hypotheses about these situational changes
4. Do research (Google, LinkedIn, Crunchbase) to find publicly visible signals
5. Use these signals to identify prospects experiencing similar changes
6. Test in campaigns and iterate

WHY THIS MATTERS:
A company doesn't wake up and decide to buy your product randomly.
Something changed. If you know what that change is, you can:
- Reach out at exactly the right time
- Lead with their current pain (not generic pitch)
- Significantly increase conversion rates

HOW TO USE:
- Reference when researching campaign targets
- Use in prompts/situational_change_extraction.md to find more examples
- Update after each campaign based on what actually worked
-->

## How to Identify Situational Changes

### In Transcripts, Listen For:

**Time-based phrases**:
- "We just..." / "Recently..." / "In the last few months..."
- "Ever since [event]..."
- "Now that we..."

**Example Quotes**:
> "We just raised our Series B and need to scale infrastructure fast"
>
> "Ever since our CTO left, we've been struggling with deployment"
>
> "We recently had an outage that cost us $50K, can't let that happen again"

### Ask: What Changed?

Categories of change:
1. **Organizational** - New executive, team growth, reorg
2. **Technical** - Migration, outage, scaling pain
3. **Business** - Funding, new product, market expansion
4. **Competitive** - Competitor launched feature, losing deals
5. **Regulatory** - New compliance requirement, audit finding

---

## Situational Change Hypotheses by Segment

### Mid-Market Fintech: Recent Funding Round

**Hypothesis**: Fintech companies that raise Series B or C are ready to invest in infrastructure.

**Why This Works**:
- They now have budget ($10M+ raised)
- Board/investors expect faster shipping
- Small eng team (10-30) can't keep building internal tools
- Growth pressure: need to scale without scaling headcount

**Evidence from Transcripts**:
- Account_023: "We just closed Series B. Our board wants us shipping 2x faster."
- Account_041: "Raised $25M last quarter. Can't keep babysitting deploys manually."
- Account_067: "Post-funding, we're hiring 20 engineers. Need to get infra right now."

**Publicly Visible Signals**:
- Crunchbase funding announcement (last 3-6 months)
- LinkedIn: Hiring for engineers/DevOps (10+ open roles)
- Press releases about growth plans

**How to Find These Companies**:
1. Monitor Crunchbase for Series B/C fintech funding
2. Check LinkedIn for hiring signals
3. Use news APIs to find press releases

**Research Tools**:
- Crunchbase API
- Google News API (search: "fintech raised series B")
- LinkedIn jobs (search: fintech companies hiring engineers)

**Conversion Rate**: 45% (vs. 30% baseline)

---

### Mid-Market Fintech: New VP Engineering or CTO

**Hypothesis**: New engineering leaders want to make an impact in first 90 days.

**Why This Works**:
- They're evaluating everything ("fresh eyes")
- Need a quick win to justify their hire
- Have budget authority or can advocate for spend
- Want to modernize stack

**Evidence from Transcripts**:
- Account_089: "I just joined as VP Eng. Looking to upgrade our deployment process."
- Account_102: "New CTO here. Our deploy process is stuck in 2015, needs to change."

**Publicly Visible Signals**:
- LinkedIn profile shows recent job change (within 3 months)
- "Pleased to announce..." posts
- Press releases about executive hire

**How to Find These Companies**:
1. LinkedIn Sales Navigator: Filter for VP Eng/CTO with "Past 90 days" start date
2. Google News: "[company] appoints new CTO"

**Conversion Rate**: 40%

---

### Mid-Market Fintech: Recent Outage or Incident

**Hypothesis**: Companies that just had a production outage are motivated to prevent the next one.

**Why This Works**:
- Pain is acute (just happened)
- Executive visibility (CEO asking "why?")
- Budget suddenly available (pain-driven purchase)
- Champion has ammunition ("this will prevent that")

**Evidence from Transcripts**:
- Account_115: "We had a deploy failure last week that took down payment processing for 2 hours. Cost us $100K. Can't happen again."
- Account_134: "Black Friday outage. CEO is personally asking about our deploy process now."

**Publicly Visible Signals**:
- Twitter/X mentions of downtime
- StatusPage incidents
- News articles about outage
- Customer complaints on social media

**How to Find These Companies**:
- Twitter/X monitoring for "[company name] down"
- StatusPage API
- Google News alerts for "outage"

**Conversion Rate**: 50% (highest of all triggers)

**Caveat**: Hard to find these signals at scale. Works best for inbound leads.

---

### SMB SaaS: First DevOps Hire

**Hypothesis**: When SMB SaaS companies post their first DevOps job, they're acknowledging deployment is a problem.

**Why This Works**:
- They've crossed threshold where manual deploy doesn't scale
- Hiring is expensive ($120K+ salary)
- They're open to "buy vs. build" conversation
- Timeline: Hiring takes 3-6 months, tool can solve pain faster

**Evidence from Transcripts**:
- Account_156: "We posted for a DevOps engineer 2 months ago, haven't found anyone. Need a faster solution."

**Publicly Visible Signals**:
- LinkedIn job postings for "DevOps", "SRE", "Infrastructure"
- Indicates: ~10-50 engineers, feeling deployment pain

**How to Find These Companies**:
- LinkedIn job search: "DevOps" at companies with 10-100 employees

**Conversion Rate**: 38%

---

## Testing Your Hypotheses

### Process:

1. **Pick a hypothesis** (e.g., "Post-funding fintech")
2. **Find companies matching criteria** using research tools
3. **Pull into campaign** (`campaigns/YYYY-MM-DD_post_funding_fintech/`)
4. **Craft targeted message** referencing the situational change
   - Subject: "Congrats on the Series B"
   - Body: "Most fintech teams we work with hit deployment bottlenecks within 6 months of raising. We help you scale without dedicating an SRE..."
5. **Measure results**: Response rate, meeting rate, close rate
6. **Update this file** with learnings

### Validation Questions:

- **Did the trigger actually matter?** (Did mentions of funding resonate?)
- **Was timing right?** (Is 3 months post-funding better than 6 months?)
- **Did we find enough accounts?** (Is this trigger scalable?)

---

## Research Workflow for Situational Changes

### Step 1: Identify Trigger from Transcripts

Use `prompts/situational_change_extraction.md` to have AI analyze transcripts:

```
Prompt: "Read these 10 transcripts from won deals in the fintech segment. What changed in their business that made them need us NOW? Look for funding, new hires, outages, growth pains."
```

### Step 2: Find Publicly Visible Signals

For the triggers you found, ask:
- "Can I see this on Crunchbase?" (funding)
- "Can I see this on LinkedIn?" (new hire, job posting)
- "Can I see this in news?" (outage, press release)

### Step 3: Build Research Snapshot

Create `research/snapshots/YYYY-MM-DD/midmarket_fintech_post_funding/`:
- `serp_results.jsonl` - Google search results for "fintech series B 2026"
- `crunchbase_data.json` - API results for recent funding
- `synthesized_findings.md` - Your analysis of patterns

### Step 4: Pull Accounts Into Campaign

Use `pipelines/campaign_pull.py` to create `pulled_customers.csv` with:
- Companies matching segment AND situational change
- Recent wins in this scenario (social proof)
- Research findings (news, funding, etc.)

---

## Compound Learning Loop

**Every campaign teaches you**:
1. Which situational changes actually matter
2. How to find them at scale
3. What messaging resonates
4. What timing is right

**Feed learnings back**:
- Update this file with what worked
- Archive research in `research/snapshots/`
- Next campaign starts smarter

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
**Change Log**: _[What changed and why]_
