# GTM Repository Method

## The Core Problem This Solves

Most go-to-market teams suffer from **knowledge fracture**:
- Each campaign starts from scratch
- Insights live in someone's head or scattered Notion docs
- Call transcripts are searchable but not synthesized
- "What worked last time?" requires asking around

This repository methodology creates a **compounding knowledge system** where every campaign makes future campaigns smarter.

## The Mental Model

### Repo-Level: Durable Foundation

The `source/` directory contains your institutional knowledge:

1. **ICP Definition** (`source/icp/`)
   - Who you sell to
   - How you win
   - What you don't do (exclusions)
   - Your positioning

2. **Persona Taxonomy** (`source/personas/`)
   - Champion, blocker, economic buyer, technical buyer, end user
   - Labels tied to real people in your CRM
   - How each persona thinks about your solution

3. **CRM Data** (`source/crm/`)
   - Historical ARR and deal data
   - Account and contact information
   - Exported regularly with timestamps
   - Derived datasets (deals_with_arr, accounts_enriched)

4. **Call Transcripts** (`source/transcripts/`)
   - Tied to deals via join keys (Salesforce ID, etc.)
   - Normalized format for analysis
   - Raw exports preserved for auditing

5. **Enrichment Data** (`source/enrichment/`)
   - Industry, headcount, tech stack
   - From Clay, Clearbit, ZoomInfo, or similar
   - Refreshed periodically to stay current

6. **Founder Context** (`source/founder_notes/`)
   - Audio notes about the market (transcribed)
   - Strategic context that isn't in transcripts
   - The "why" behind product and market decisions

### Analysis: Pattern Recognition

The `analysis/` directory is where you synthesize insights:

1. **Segmentation** (`analysis/segmentation/`)
   - Segment hypotheses (e.g., "mid-market fintech 200-1k headcount")
   - Rules for bucketing accounts (SMB, mid-market, enterprise)
   - Evidence from past wins

2. **Situational Changes** (`analysis/situational_changes/`)
   - What changed in their business that made them buy NOW
   - Common triggers: funding events, new hire, compliance deadline, tool failure
   - Evidence table with citations back to transcripts

3. **Win/Loss Themes** (`analysis/win_loss/`)
   - Why you win (differentiators)
   - Common objections and how they're handled
   - Where you lose and to whom

### Campaign-Level: Execution with Context

Each campaign in `campaigns/` is a working set:

1. **Pull Context** from source and analysis
   - Define target segment and personas
   - Pull relevant customers who match the profile
   - Reference past wins in this segment

2. **Do Campaign-Specific Research**
   - News about target accounts
   - Funding events, leadership changes, tech stack shifts
   - Store in `research/snapshots/YYYY-MM-DD/`

3. **Generate Messaging Hypotheses**
   - What situational change are we responding to?
   - How do we position against alternatives?
   - What's the hook in the first email?

4. **Execute and Track**
   - Outreach log (who, when, which sequence)
   - Replies and outcomes (JSONL for easy append)
   - Decisions made during the campaign

5. **Feed Learnings Back**
   - What worked? What didn't?
   - New objections discovered?
   - Should this segment be refined?
   - Write `results/learnings.md` and roll it into `analysis/` or `source/`

## Key Design Choices

### 1. File-Based, Not Database

Everything is CSV, JSON, JSONL, Parquet, or Markdown. Why?
- Versioned with Git
- Easy to diff and review
- No database to maintain
- Works with any data tool (pandas, duckdb, Excel)

### 2. Dated Snapshots

Raw exports and research are timestamped:
- `crm_deals_2026-01-10.csv`
- `research/snapshots/2026-01-10/`

This preserves historical context. You can recreate analysis from any point in time.

### 3. Normalized + Raw

Keep both:
- **Raw**: Exactly what came from the source system
- **Normalized**: Cleaned, joined, standardized schema

Raw is for auditing. Normalized is for analysis.

### 4. Join Keys Everywhere

Document identifiers in `source/joins/keys.md`:
- Salesforce Account ID
- Salesforce Opportunity ID
- Gong Call ID
- Email hash (for privacy-preserving joins)

Every dataset should be joinable.

### 5. Prompts Are Code

Reusable prompts live in `prompts/`:
- `segmentation.md` - How to segment customers
- `situational_change_extraction.md` - How to find "what changed"
- `messaging_generation.md` - How to draft sequences

Treat prompts like code: version them, review them, improve them.

## The Compounding Loop

```
1. Ingest CRM/transcripts/enrichment → source/
2. Run analysis → analysis/
3. Start campaign with context → campaigns/YYYY-MM-DD_name/
4. Execute campaign → results/
5. Extract learnings → results/learnings.md
6. Roll learnings back → analysis/ and source/
7. Repeat (with more context than last time)
```

Each loop:
- Improves your segment definitions
- Surfaces more situational changes
- Refines your messaging
- Updates your ICP understanding

## Success Metrics for This Methodology

You know this is working when:
- New campaigns reference 3+ past campaigns in their brief
- Segment definitions have evidence citations
- Messaging hypotheses cite specific transcripts
- Win/loss themes are updated monthly
- Founders can query this repo to understand the market

## Anti-Patterns to Avoid

❌ **One-off analysis in a notebook that never gets saved**
- Always export to `analysis/` or `outputs/`

❌ **Campaigns that don't write learnings.md**
- Knowledge dies if not recorded

❌ **Stale source data**
- Set calendar reminders to refresh CRM and enrichment

❌ **No join keys**
- Document how datasets connect, or you'll lose ability to cross-reference

❌ **Prompts scattered in ChatGPT history**
- Copy working prompts into `prompts/` immediately

## Getting Started (Minimal v0)

If you're starting from scratch:

1. **Export your CRM** → `source/crm/exports/`
2. **Define your ICP** → `source/icp/icp.md`
3. **List your personas** → `source/personas/personas.yaml`
4. **Pick one segment to test** → `analysis/segmentation/segments.md`
5. **Run one campaign** → `campaigns/2026-01-10_test/`
6. **Write what you learned** → `campaigns/2026-01-10_test/results/learnings.md`

Then repeat with more context each time.

---

**The goal**: Make it impossible to do one-off work. Every action should make the next action easier.
