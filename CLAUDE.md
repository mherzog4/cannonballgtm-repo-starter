# CLAUDE.md - AI Assistant Guidelines

## Repository Purpose

This is a Go-To-Market (GTM) knowledge repository designed for **compounding learning**. Every artifact created here should be reusable, versioned, and contribute to institutional knowledge.

## Core Principles

### 1. Never Do One-Off Work
- All analysis must produce saved artifacts
- All research must be snapshotted and dated
- All campaign learnings must be rolled back into source data or analysis folders

### 2. Data Flow Architecture
```
source/           → Source of truth (ICP, personas, CRM, transcripts)
analysis/         → Insights derived from source data
research/         → External data snapshots (dated)
campaigns/        → Working sets that pull from source + analysis
campaigns/*/learnings.md → Feeds back into analysis/ and source/
```

### 3. Privacy & Redaction
- Before committing transcripts or CRM data, check `docs/privacy_and_redaction.md`
- PII (emails, phone numbers, specific names) should be redacted or hashed
- Focus on preserving signal (job titles, industries, deal patterns) while removing identifiers

## Working with This Repo

### When Ingesting New Data
1. Save raw data with timestamp: `source/crm/exports/crm_deals_YYYY-MM-DD.csv`
2. Document schema in `source/*/schemas/`
3. Create normalized/derived versions in `source/*/derived/`
4. Update `source/joins/keys.md` if new identifiers are introduced

### When Running Analysis
1. Document methodology in the analysis folder (e.g., `analysis/segmentation/segments.md`)
2. Include evidence and citations back to source data
3. Export tables to `analysis/*/` with clear names
4. Create hypotheses that can be tested in campaigns

### When Starting a Campaign
1. Create dated folder: `campaigns/YYYY-MM-DD_description/`
2. Define segment in `segment.yaml` (references `analysis/segmentation/`)
3. Pull relevant source data into `pulled_customers.csv`
4. Document decisions in `decisions.md`
5. Track results in `results/outreach_log.csv` and `results/replies.jsonl`
6. **Critical**: Write `results/learnings.md` at campaign end

### When Writing Prompts
- Store reusable prompts in `prompts/`
- Reference source data structure and schemas
- Include examples of good outputs
- Version prompts if they change significantly

## File Naming Conventions

- **Dates**: Use `YYYY-MM-DD` format
- **Exports**: Include date suffix (e.g., `accounts_enriched_2026-01-10.csv`)
- **Derived data**: Use `.parquet` for efficiency when file size matters
- **Logs**: Use `.jsonl` for append-only event streams

## ID Joining Strategy

All datasets should be joinable via consistent identifiers documented in `source/joins/keys.md`. Common keys:
- `salesforce_account_id`
- `salesforce_opportunity_id`
- `gong_call_id`
- `email_hash` (for privacy-preserving joins)

## What AI Assistants Should Do

✅ Help segment customers based on source data
✅ Extract situational changes from transcripts
✅ Generate messaging hypotheses for campaigns
✅ Analyze campaign results and suggest iterations
✅ Create evidence tables linking hypotheses to data
✅ Suggest when to roll campaign learnings back into source/

## What AI Assistants Should NOT Do

❌ Make up data or hallucinate customer examples
❌ Commit PII without redaction
❌ Create one-off analysis that doesn't get saved
❌ Bypass the master → analysis → campaign flow
❌ Ignore existing schemas and naming conventions

## How to Compound Knowledge

After each campaign:
1. Update `analysis/win_loss/` with new themes
2. Refine `analysis/segmentation/` if new patterns emerge
3. Add situational changes to `analysis/situational_changes/evidence_table.csv`
4. Consider updating `source/icp/` if market understanding shifted
5. Improve `prompts/` based on what worked

## Pipeline Execution Order

```
1. ingest_crm.py          → source/crm/derived/
2. ingest_transcripts.py  → source/transcripts/normalized/
3. enrich_accounts.py     → source/enrichment/outputs/
4. segment.py             → analysis/segmentation/
5. extract_situational_changes.py → analysis/situational_changes/
6. campaign_pull.py       → campaigns/*/pulled_customers.csv
7. [Run campaign manually]
8. evaluate_campaign_results.py → campaigns/*/results/learnings.md
```

## Questions to Ask Before Taking Action

- Does this create a reusable artifact?
- Is this data snapshot dated and stored?
- Can someone reproduce this analysis in 6 months?
- Am I preserving the join keys for later use?
- Should this learning update the source data?

---

**Remember**: The goal is to make it impossible to lose knowledge. Every insight should have a permanent home in this repo.
