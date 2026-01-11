# Prompt: Situational Change Extraction

<!--
PURPOSE: Extract "what changed" from transcripts to identify buying triggers.
Use this prompt with AI to analyze won deal transcripts and find patterns.

HOW TO USE:
1. Load transcripts from source/transcripts/normalized/
2. Filter to won deals in a specific segment
3. Run this prompt against those transcripts
4. Output becomes input for analysis/situational_changes/hypotheses.md

THE GOAL:
Find the answer to: "What changed in their business that made them need us NOW?"
-->

## Prompt Template

```
You are analyzing sales call transcripts to identify situational changes that created a buying window.

CONTEXT:
- These are transcripts from CLOSED-WON deals
- Segment: [INSERT SEGMENT, e.g., "Mid-Market Fintech"]
- Time period: [INSERT DATE RANGE]

YOUR TASK:
Read the transcripts and identify what changed in the prospect's business that made them actively looking for a solution NOW (vs. 6 months ago when they weren't).

LOOK FOR THESE CATEGORIES OF CHANGE:

1. ORGANIZATIONAL CHANGES
   - New executive (VP Eng, CTO, etc.)
   - Team growth (hiring surge)
   - Reorg or new team structure

2. TECHNICAL CHANGES
   - Migration (cloud, tech stack)
   - Recent outage or production incident
   - Scaling pain (infrastructure breaking down)
   - Deprecation of old tool

3. BUSINESS CHANGES
   - Funding round (Series A/B/C)
   - New product launch
   - Market expansion
   - Acquisition or merger

4. COMPETITIVE CHANGES
   - Competitor launched feature
   - Losing deals due to tech debt
   - Market pressure to ship faster

5. REGULATORY/COMPLIANCE CHANGES
   - New compliance requirement (SOC 2, GDPR)
   - Audit finding
   - Security incident

LISTEN FOR PHRASES LIKE:
- "We just..." / "Recently..." / "In the last few months..."
- "Ever since [event]..."
- "Now that we..."
- "After [event] happened..."
- "[Person] joined and..."

OUTPUT FORMAT:

For each transcript, provide:

**Account ID**: [from transcript metadata]
**Opportunity ID**: [from transcript metadata]
**Situational Change Category**: [one of the 5 categories above]
**Specific Change**: [1-2 sentence description]
**Evidence Quote**: [exact quote from transcript]
**Timing**: [how long ago did this change happen?]
**Publicly Visible?**: [Yes/No - can we find this on LinkedIn, Crunchbase, news?]

---

EXAMPLE OUTPUT:

**Account ID**: Account_023
**Opportunity ID**: 006XYZ
**Situational Change Category**: Business Change
**Specific Change**: Closed Series B funding round 3 months before first call
**Evidence Quote**: "We just closed Series B. Our board wants us shipping 2x faster and we can't keep manually deploying."
**Timing**: 3 months ago
**Publicly Visible?**: Yes (Crunchbase, press release)

---

After analyzing all transcripts, provide:

**PATTERN SUMMARY**:
- Most common situational change: [X] (appears in Y% of transcripts)
- Second most common: [X] (appears in Y% of transcripts)
- Average timing: Change happened [X] weeks/months before first contact

**RESEARCH RECOMMENDATIONS**:
- To find more companies with [situational change], look for: [specific signals]
- Sources to monitor: [Crunchbase, LinkedIn, news, etc.]

```

## Input Data

**Load transcripts**:
```python
import pandas as pd

# Load transcripts
df = pd.read_parquet('source/transcripts/normalized/transcripts.parquet')

# Join with opportunities to get win/loss data
opps = pd.read_csv('source/crm/exports/crm_deals_YYYY-MM-DD.csv')
df = df.merge(opps, on='opportunity_id')

# Filter to won deals in target segment
df_won = df[(df['is_won'] == True) & (df['segment'] == 'midmarket_fintech')]

# Select a sample (e.g., 10 transcripts)
sample = df_won.head(10)

# Export for AI analysis
sample[['transcript_id', 'opportunity_id', 'account_id', 'transcript_text']].to_json(
    'temp_transcripts_for_analysis.jsonl',
    orient='records',
    lines=True
)
```

## Running with Claude Code or ChatGPT

```bash
# Copy prompt + transcript data into Claude Code / ChatGPT
cat prompts/situational_change_extraction.md
cat temp_transcripts_for_analysis.jsonl

# Or use Claude's API in batch mode for efficiency
```

## Output Destination

Save analysis results to:
- `analysis/situational_changes/evidence_table.csv` (structured data)
- `analysis/situational_changes/hypotheses.md` (narrative summary)

## Iteration

After first pass:
1. Look for patterns (which changes are most common?)
2. Research: Can you find these signals publicly?
3. Create hypothesis for next campaign
4. Test and measure
5. Refine this prompt based on what you learn

---

**Version**: v1.0
**Last Updated**: _[YYYY-MM-DD]_
