# Join Keys Documentation

<!--
PURPOSE: Document how different datasets connect to each other.
This is critical for cross-referencing data across source files.

HOW TO USE:
- Reference when writing queries that span multiple datasets
- Update when adding new data sources
- Use as guide for creating mapping tables when IDs don't match

THE WORKFLOW:
Your CRM, transcripts, and enrichment data need to connect via join keys.
The most important joins are:
1. Transcripts → Deals (via opportunity_id)
2. Transcripts → Accounts (via account_id)
3. Enrichment → Accounts (via account_name or domain)
4. Personas → Contacts (via email_hash)

Without clean join keys, you can't answer questions like:
"What do champions say in discovery calls for mid-market fintech deals?"
-->

## Primary Join Keys

### CRM-to-CRM Joins

| From | To | Join Key | Type |
|------|----|-----------| --- |
| Opportunities | Accounts | `account_id` | 1-to-many (one account, many deals) |
| Contacts | Accounts | `account_id` | 1-to-many (one account, many contacts) |
| Contacts | Opportunities | `opportunity_id` + `contact_id` via contact_role junction table | many-to-many |

**Example Query**:
```sql
-- Get all contacts involved in a deal
SELECT
    c.contact_id,
    c.job_title,
    o.opportunity_id,
    o.stage,
    o.amount
FROM contacts c
JOIN accounts a ON c.account_id = a.account_id
JOIN opportunities o ON a.account_id = o.account_id
WHERE o.opportunity_id = '0061234567ABCDEFGH'
```

### Transcript-to-CRM Joins

| From | To | Join Key | Notes |
|------|----|----------|-------|
| Transcripts | Opportunities | `opportunity_id` | **Best join** - direct link from Gong/Chorus to Salesforce |
| Transcripts | Accounts | `account_id` | Use if opportunity_id not available |

**Example Query**:
```sql
-- Get all calls for a specific deal
SELECT
    t.transcript_id,
    t.call_date,
    t.transcript_text,
    o.stage,
    o.amount
FROM transcripts t
JOIN opportunities o ON t.opportunity_id = o.opportunity_id
WHERE o.opportunity_id = '0061234567ABCDEFGH'
ORDER BY t.call_date
```

**Troubleshooting**: If `opportunity_id` is missing from transcripts:
1. Check if your call recording tool is configured to sync with CRM
2. Create manual mapping in `source/joins/mappings/salesforce_to_gong_mapping.csv`
3. Or join by `account_id` + date range (calls during deal window)

### Enrichment-to-CRM Joins

| From | To | Join Key | Notes |
|------|----|----------|-------|
| Enrichment | Accounts | `account_name` | **Fuzzy match needed** - names rarely match exactly |
| Enrichment | Accounts | `domain` | **Best join** if both have domain field |

**Example Query** (with fuzzy matching):
```python
import pandas as pd
from fuzzywuzzy import process

crm = pd.read_csv('source/crm/exports/crm_accounts_2026-01-10.csv')
enrichment = pd.read_csv('source/enrichment/outputs/accounts_enriched_2026-01-10.csv')

# Fuzzy match account names
def find_best_match(name, choices, threshold=80):
    match = process.extractOne(name, choices)
    return match[0] if match and match[1] >= threshold else None

crm['enrichment_match'] = crm['account_name'].apply(
    lambda name: find_best_match(name, enrichment['company_name'].tolist())
)

# Join on matched names
merged = crm.merge(
    enrichment,
    left_on='enrichment_match',
    right_on='company_name',
    how='left'
)
```

**Best Practice**: Create a manual mapping table for your top 100 accounts:

`source/joins/mappings/crm_to_enrichment_mapping.csv`:
```csv
account_id,crm_account_name,enrichment_company_name
0011234567ABCDEFGH,Acme Corporation,Acme Corp
0012345678ABCDEFGH,Globex Inc.,Globex
```

### Persona-to-Contact Joins

| From | To | Join Key | Notes |
|------|----|----------|-------|
| Persona Labels | Contacts | `email_hash` | Privacy-safe join (no raw emails exposed) |

**Example Query**:
```sql
-- Get all champions at an account
SELECT
    c.contact_id,
    c.job_title,
    p.persona_label,
    a.account_name
FROM contacts c
JOIN persona_labels p ON c.email_hash = p.email_hash
JOIN accounts a ON c.account_id = a.account_id
WHERE p.persona_label = 'Champion'
  AND a.account_id = '0011234567ABCDEFGH'
```

**How to create email_hash**:
```python
import hashlib

def hash_email(email):
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()

df['email_hash'] = df['email'].apply(hash_email)
```

## Complex Joins (Multi-Hop)

### "What do champions say in discovery calls for mid-market fintech deals?"

This requires joining:
1. Opportunities (filter: closed-won, mid-market segment, fintech industry)
2. → Transcripts (filter: call_type = 'discovery')
3. → Contacts (via transcript speakers)
4. → Persona Labels (filter: persona_label = 'Champion')

```sql
SELECT
    t.transcript_text,
    o.opportunity_id,
    a.account_name,
    a.industry,
    a.headcount
FROM transcripts t
JOIN opportunities o ON t.opportunity_id = o.opportunity_id
JOIN accounts a ON o.account_id = a.account_id
WHERE a.industry = 'Fintech'
  AND a.headcount BETWEEN 200 AND 1000  -- Mid-market
  AND o.is_won = true
  AND t.call_type = 'discovery'
  AND t.speakers LIKE '%Champion%'  -- Or join to persona_labels
```

### "Which segments have the highest win rate?"

```sql
SELECT
    a.segment,
    COUNT(DISTINCT o.opportunity_id) as total_deals,
    SUM(CASE WHEN o.is_won THEN 1 ELSE 0 END) as won_deals,
    ROUND(AVG(CASE WHEN o.is_won THEN 1.0 ELSE 0.0 END) * 100, 2) as win_rate_pct
FROM accounts a
JOIN opportunities o ON a.account_id = o.account_id
WHERE o.is_closed = true
GROUP BY a.segment
ORDER BY win_rate_pct DESC
```

## When Join Keys Are Missing

### Problem: Transcripts don't have opportunity_id

**Solutions**:

1. **Join by account + date range**:
```sql
SELECT t.*, o.*
FROM transcripts t
JOIN opportunities o
    ON t.account_id = o.account_id
    AND t.call_date BETWEEN o.created_date AND o.close_date
```

2. **Create manual mapping table**:
`source/joins/mappings/salesforce_opportunity_to_gong_call.csv`:
```csv
opportunity_id,transcript_id,mapped_by,mapped_date
0061234567ABCDEFGH,call_a7b3c9d2-...,manual,2026-01-10
```

3. **Use AI to help map**:
```
Prompt: "I have a deal for Acme Corp that closed in Q4 2025. Find calls with Acme Corp between Oct 1 and Dec 31, 2025. Which calls likely belong to this deal based on call content?"
```

### Problem: Enrichment names don't match CRM names

**Solutions**:

1. **Use domain matching** (if both have website field)
2. **Fuzzy string matching** (FuzzyWuzzy, RapidFuzz)
3. **Create mapping table for top accounts** (manual but reliable)

## Data Flow Diagram

```
CRM (source/crm/)
├── Accounts → [account_id] → Opportunities
├── Accounts → [account_id] → Contacts
├── Contacts → [email_hash] → Persona Labels (source/personas/)
└── Opportunities → [opportunity_id] → Transcripts (source/transcripts/)

Enrichment (source/enrichment/)
└── → [account_name or domain] → Accounts (fuzzy match)

Analysis (analysis/)
├── Segmentation → Uses: Accounts + Enrichment
├── Situational Changes → Uses: Transcripts + Opportunities
└── Win/Loss → Uses: Transcripts + Opportunities + Persona Labels
```

## Best Practices

1. **Always use join keys, never business names**
   - ❌ Join on `account_name` (names change, have typos)
   - ✅ Join on `account_id` (stable unique identifier)

2. **Document custom mappings**
   - Store in `source/joins/mappings/`
   - Include `mapped_by` (who), `mapped_date` (when)

3. **Validate joins**
   - Check for duplicates after joining
   - Look for missing data (left join shows nulls)

4. **Keep schemas in sync**
   - When CRM fields change, update `source/crm/schemas/`
   - Update this file if join keys change

## Updating This File

**When to update**:
- Adding new data source
- Changing join logic
- Creating new mapping tables

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
