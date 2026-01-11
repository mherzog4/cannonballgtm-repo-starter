# GTM Repository Starter

A file-based, Git-versioned system for building **compounding knowledge** in your go-to-market processes.

## The Problem This Solves

Most GTM teams suffer from **knowledge fracture**:
- Each campaign starts from scratch
- Insights live in someone's head or scattered docs
- Call transcripts are searchable but not synthesized
- "What worked last time?" requires tribal knowledge

This repository provides a methodology where **every campaign makes future campaigns smarter**.

## Core Principles

### 1. Source of Truth (`source/`)
Your durable foundation:
- ICP definition (who you sell to, how you win)
- Persona taxonomy (champion, blocker, economic buyer)
- CRM data with historical ARR
- Enrichment data (industry, headcount, tech stack)
- Call transcripts tied to deals
- Founder/leadership market notes

### 2. Analysis (`analysis/`)
Insights derived from source data:
- **Segmentation**: Pattern recognition in your best customers
- **Situational Changes**: What triggers buying (funding, new hire, outage)
- **Win/Loss Themes**: Why you win, why you lose, objection handling

### 3. Research (`research/`)
External data snapshots:
- Dated research (Crunchbase, LinkedIn, news)
- Stored so future campaigns can reference

### 4. Campaigns (`campaigns/`)
Working sets for specific motions:
- Pull context from source + analysis
- Do campaign-specific research
- Generate messaging hypotheses
- **Critical**: Feed learnings back via `learnings.md`

## The Compounding Loop

```
1. Ingest source data (CRM, transcripts, enrichment)
2. Run analysis (segments, situational changes)
3. Start campaign with full context
4. Execute and track results
5. Document learnings
6. Feed back to analysis/ and source/
7. Next campaign starts smarter → REPEAT
```

Each iteration improves:
- Segment definitions get sharper
- Situational triggers become predictable
- Messaging becomes more targeted
- Win rates increase

## Repository Structure

```
gtm-repo/
├── README.md
├── CLAUDE.md                    # AI assistant guidelines
├── docs/                        # Methodology docs
│   ├── method.md
│   ├── data_dictionary.md
│   ├── id_joining.md
│   └── privacy_and_redaction.md
├── source/                      # Source of truth
│   ├── icp/                     # Ideal customer profile
│   ├── personas/                # Persona definitions & labels
│   ├── crm/                     # CRM exports & derived data
│   ├── transcripts/             # Call recordings
│   ├── enrichment/              # External data (Clay, Clearbit)
│   ├── founder_notes/           # Strategic context
│   └── joins/                   # How datasets connect
├── analysis/                    # Insights
│   ├── segmentation/            # Customer segments
│   ├── situational_changes/    # Buying triggers
│   └── win_loss/                # Why you win/lose
├── research/                    # External research
│   ├── tools/                   # Research tool docs
│   └── snapshots/               # Dated research exports
├── prompts/                     # Reusable AI prompts
├── pipelines/                   # Automation scripts
└── campaigns/                   # Campaign execution
    └── YYYY-MM-DD_name/
        ├── brief.md
        ├── segment.yaml
        ├── pulled_customers.csv
        ├── research/
        ├── hypotheses/
        ├── assets/
        ├── results/
        │   └── learnings.md     # ← CRITICAL: Feed back to analysis/
        └── decisions.md
```

## Getting Started

### 1. Clone and Customize

```bash
git clone [your-repo-url]
cd gtm-repo
```

### 2. Populate Source Data

```bash
# Export your CRM to source/crm/exports/
# Format: crm_accounts_YYYY-MM-DD.csv, crm_deals_YYYY-MM-DD.csv, etc.

# Define your ICP
# Edit source/icp/icp.md with your actual customer profile

# Define personas
# Edit source/personas/persona_taxonomy.md
```

### 3. Ingest and Segment

```bash
# Install dependencies
pip install pandas pyyaml pyarrow

# Ingest CRM data
python pipelines/ingest_crm.py \
  --accounts source/crm/exports/crm_accounts_YYYY-MM-DD.csv \
  --opportunities source/crm/exports/crm_deals_YYYY-MM-DD.csv \
  --contacts source/crm/exports/crm_contacts_YYYY-MM-DD.csv

# Classify accounts into segments
python pipelines/segment.py \
  --input source/crm/derived/accounts.parquet \
  --output source/crm/derived/accounts_with_segments.parquet
```

### 4. Analyze Transcripts

Use `prompts/situational_change_extraction.md` with Claude or ChatGPT to find buying triggers:

```bash
# Export transcripts from Gong/Chorus to source/transcripts/raw/
# Use AI to analyze: "What changed in their business that made them buy NOW?"
# Document findings in analysis/situational_changes/
```

### 5. Run Your First Campaign

```bash
# Pull target accounts
python pipelines/campaign_pull.py \
  --campaign campaigns/YYYY-MM-DD_your_campaign_name

# Generate messaging using prompts/messaging_generation.md
# Execute campaign
# Track results
# **DOCUMENT LEARNINGS** in results/learnings.md
```

### 6. The Critical Step: Feed Learnings Back

After each campaign:
1. Write `campaigns/*/results/learnings.md`
2. Update `analysis/` with new patterns
3. Refine `source/icp/` if needed
4. Commit to Git
5. Next campaign inherits this knowledge

## Key Design Choices

### File-Based, Not Database
- Everything is CSV, JSON, Parquet, or Markdown
- Versioned with Git
- Easy to diff and review
- Works with any tool (pandas, Excel, duckdb)

### Dated Snapshots
- All exports timestamped: `crm_deals_2026-01-15.csv`
- Research dated: `research/snapshots/2026-01-15/`
- Preserves historical context

### Privacy First
- See `docs/privacy_and_redaction.md`
- Hash emails before committing
- Never commit raw PII
- Redaction scripts included

### Prompts as Code
- Reusable prompts in `prompts/`
- Version them, review them, improve them
- Treat like any other code artifact

## What Makes This "Compounding"

Traditional GTM tools (Clay, Outreach, etc.) are **stateless** - each table or sequence exists in isolation.

This repo is **stateful** - it accumulates knowledge:
- Segment definitions cite evidence from past wins
- Situational triggers are validated across campaigns
- Messaging improves based on what actually worked
- New campaigns reference 3+ previous campaigns

**The goal**: Make it impossible to lose knowledge.

## Anti-Patterns to Avoid

❌ One-off analysis in a notebook that never gets saved
❌ Campaigns without `learnings.md`
❌ Stale source data (set calendar reminders)
❌ No join keys documented
❌ Prompts scattered in ChatGPT history

## Prerequisites

- Python 3.8+ (for pipelines)
- CRM access (Salesforce, HubSpot, etc.)
- Call recording tool (Gong, Chorus, etc.)
- Enrichment data (Clay, Clearbit, ZoomInfo)
- Git basics

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Guidelines for AI assistants
- **[docs/method.md](docs/method.md)** - Full methodology explanation
- **[docs/data_dictionary.md](docs/data_dictionary.md)** - Data field reference
- **[docs/id_joining.md](docs/id_joining.md)** - How to connect datasets
- **[docs/privacy_and_redaction.md](docs/privacy_and_redaction.md)** - PII guidelines

## Example Use Cases

- **B2B SaaS**: Target mid-market companies post-Series B funding
- **Fintech**: Reach out after regulatory changes or audit findings
- **DevTools**: Target companies posting DevOps job openings
- **Enterprise**: Engage with companies after new CTO hire

## Contributing

This is an open-source template. Contributions welcome:
- Improved pipeline scripts
- Additional prompt templates
- Documentation improvements
- Example campaigns

Please open an issue before submitting major changes.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

This methodology is inspired by the practice of treating GTM data like a software engineering codebase - versioned, compound, and collaborative.

---

**Start here**: Read [docs/method.md](docs/method.md) for the full methodology, then customize [source/icp/icp.md](source/icp/icp.md) with your ICP.
