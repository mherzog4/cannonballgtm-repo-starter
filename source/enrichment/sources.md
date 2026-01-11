# Enrichment Data Sources

<!--
PURPOSE: Document where your enrichment data comes from and how to refresh it.
Enrichment adds firmographic data (industry, headcount, tech stack) to CRM accounts.

HOW TO USE:
- Reference when setting up enrichment pipelines
- Update when adding new data sources
- Track refresh schedule to keep data current
-->

## Active Enrichment Sources

### Clay (Primary Enrichment)

**What We Get**:
- Industry classification
- Employee headcount
- Tech stack (via BuiltWith integration)
- Funding data (via Crunchbase integration)
- Contact enrichment (job titles, LinkedIn profiles)

**How to Access**:
- Clay account: [your account]
- API docs: https://clay.com/docs

**Refresh Frequency**: Weekly (every Monday)

**Cost**: $X/month for Y credits

**Data Quality**:
- Coverage: ~85% of accounts have industry + headcount
- Accuracy: ~90% based on spot checks

**Pipeline**: `pipelines/enrich_accounts.py`

---

### Clearbit (Secondary)

**What We Get**:
- Company domain and metadata
- Industry (more specific than Clay)
- Estimated revenue

**When to Use**: When Clay data is missing

**Refresh Frequency**: Monthly

---

### BuiltWith (Tech Stack)

**What We Get**:
- Technologies used (AWS, GCP, React, etc.)
- CMS platform
- Analytics tools

**Why This Matters**:
- Indicates cloud-native (AWS/GCP = good fit)
- Shows technical sophistication

**Refresh Frequency**: Quarterly (tech stacks don't change often)

---

### Crunchbase (Funding Data)

**What We Get**:
- Funding rounds (Series A/B/C)
- Funding dates
- Funding amounts
- Investors

**Why This Matters**:
- "Post-funding" situational trigger
- Budget indicator

**Access**: Via Clay integration or direct API

**Refresh Frequency**: Weekly (monitor new funding announcements)

---

### LinkedIn (via Clay)

**What We Get**:
- Employee growth rate (hiring surge indicator)
- Job postings (hiring for DevOps/SRE?)
- Executive changes (new VP Eng/CTO)

**Why This Matters**:
- Hiring surge = scaling pain
- Job postings = acknowledged need
- Executive changes = buying window

**Refresh Frequency**: Weekly

---

## Enrichment Workflow

### 1. Export CRM Accounts
```bash
# Export accounts from CRM
# Save to source/enrichment/inputs/accounts_to_enrich.csv

# Required columns: account_id, account_name, domain (if available)
```

### 2. Run Enrichment Pipeline
```bash
python pipelines/enrich_accounts.py \
  --input source/enrichment/inputs/accounts_to_enrich.csv \
  --output source/enrichment/outputs/accounts_enriched_YYYY-MM-DD.csv
```

### 3. Review and Merge
```python
# Load enrichment output
enriched = pd.read_csv('source/enrichment/outputs/accounts_enriched_2026-01-15.csv')

# Merge back to CRM accounts
accounts = pd.read_csv('source/crm/exports/crm_accounts_2026-01-15.csv')
merged = accounts.merge(enriched, on='account_id', how='left')

# Save to derived folder
merged.to_parquet('source/crm/derived/accounts_enriched.parquet', index=False)
```

### 4. Validate Data Quality
- Spot-check: Do enriched headcounts match LinkedIn?
- Coverage: What % of accounts have enrichment data?
- Update this doc if quality issues found

---

## Data Fields Added by Enrichment

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `industry` | string | Clay | Industry classification (e.g., "Fintech") |
| `headcount` | integer | Clay | Number of employees |
| `revenue_range` | string | Clearbit | Estimated revenue (e.g., "$10M-$50M") |
| `tech_stack` | array | BuiltWith | Technologies used |
| `funding_stage` | string | Crunchbase | Latest funding round (e.g., "Series B") |
| `last_funding_date` | date | Crunchbase | Date of last funding |
| `last_funding_amount` | integer | Crunchbase | Amount raised |
| `employee_growth_6mo` | decimal | LinkedIn | % employee growth (6 months) |
| `recent_job_postings` | integer | LinkedIn | Count of open eng roles |

---

## Cost Management

**Monthly Budget**: $X for enrichment

**Optimization Tips**:
- Only enrich accounts in target segments (don't enrich everything)
- Refresh high-priority accounts weekly, others monthly
- Use cached data when possible (don't re-enrich every week)

---

## Updating This File

**When to update**:
- Adding new enrichment source
- Changing refresh frequency
- Discovering data quality issues
- Updating cost/budget

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name]_
