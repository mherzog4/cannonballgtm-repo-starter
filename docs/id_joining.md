# ID Joining Strategy

<!--
PURPOSE: This file documents how different datasets connect to each other.
Without consistent join keys, you can't link transcripts to deals,
or enrichment data to accounts.

HOW TO USE:
- Reference this when writing queries that join multiple datasets
- Update when adding new data sources
- Document the mapping logic when IDs don't match 1:1

WHEN TO UPDATE:
- When ingesting a new data source with new identifiers
- When you create derived mapping tables
- When you discover ID mismatches that need manual mapping
-->

## Core Join Keys

### Primary Identifiers

| Key Name | Format | Example | Used In | Description |
|----------|--------|---------|---------|-------------|
| `salesforce_account_id` | 18-char string | `0011234567ABCDEFGH` | CRM exports, enrichment | Unique account identifier from Salesforce |
| `salesforce_opportunity_id` | 18-char string | `0061234567ABCDEFGH` | CRM exports, transcripts | Unique deal identifier from Salesforce |
| `salesforce_contact_id` | 18-char string | `0031234567ABCDEFGH` | CRM exports | Unique contact identifier from Salesforce |
| `gong_call_id` | UUID | `a7b3c9d2-...` | Transcripts | Unique call identifier from Gong |
| `email_hash` | SHA256 hash | `7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069` | Privacy-safe joins | Hashed email for joining without exposing PII |

### How to Hash Emails

For privacy-safe joins:
```python
import hashlib

def hash_email(email: str) -> str:
    # Normalize: lowercase and strip whitespace
    normalized = email.lower().strip()
    # SHA256 hash
    return hashlib.sha256(normalized.encode()).hexdigest()
```

**Important**: Always normalize before hashing (lowercase, strip whitespace) or joins will fail.

## Common Join Patterns

### 1. Link Transcripts to Deals

**Goal**: See which calls belong to which opportunity.

```sql
SELECT
    t.transcript_id,
    t.call_date,
    o.opportunity_id,
    o.stage,
    o.amount
FROM transcripts t
INNER JOIN opportunities o
    ON t.opportunity_id = o.opportunity_id
```

**Requirement**: Gong must be configured to log Salesforce Opportunity ID in call metadata.

**If this join is failing**: Check `source/transcripts/normalized/transcripts.parquet` for `opportunity_id` field. If missing, you may need to map by account + date range.

### 2. Enrich Accounts with External Data

**Goal**: Add firmographic data (industry, headcount) to CRM accounts.

```sql
SELECT
    a.account_id,
    a.account_name,
    e.industry,
    e.headcount,
    e.tech_stack
FROM accounts a
LEFT JOIN enrichment e
    ON a.account_name = e.company_name  -- Fuzzy match may be needed
```

**Warning**: Account names from CRM often don't match exactly with enrichment providers.
- CRM: `"Acme Corporation"`
- Enrichment: `"Acme Corp"`

**Solution**: Use domain matching where possible, or create a manual mapping table in `source/joins/mappings/`.

### 3. Link Personas to Contacts

**Goal**: Label which contacts are champions, blockers, etc.

```sql
SELECT
    c.contact_id,
    c.job_title,
    p.persona_label
FROM contacts c
LEFT JOIN persona_labels p
    ON c.email_hash = p.email_hash
```

**Data flow**:
1. Export contacts from CRM → `source/crm/exports/crm_contacts_YYYY-MM-DD.csv`
2. Hash emails → Add `email_hash` column
3. Manually label personas → `source/personas/persona_labels.csv`
4. Join on `email_hash`

### 4. Segment Analysis by Win Rate

**Goal**: Calculate win rate per segment.

```sql
SELECT
    a.segment,
    COUNT(DISTINCT o.opportunity_id) as total_deals,
    SUM(CASE WHEN o.is_won THEN 1 ELSE 0 END) as won_deals,
    AVG(CASE WHEN o.is_won THEN 1.0 ELSE 0.0 END) as win_rate
FROM accounts a
INNER JOIN opportunities o ON a.account_id = o.account_id
WHERE o.is_closed = true
GROUP BY a.segment
```

## Mapping Tables

When IDs don't match cleanly, create mapping tables in `source/joins/mappings/`.

### Example: `salesforce_to_gong_mapping.csv`

| salesforce_opportunity_id | gong_call_id | mapped_by | mapped_date |
|---------------------------|--------------|-----------|-------------|
| 0061234567ABCDEFGH | a7b3c9d2-... | manual | 2026-01-10 |
| 0061234567ABCDEFIJ | b8c4d0e3-... | auto | 2026-01-10 |

**Columns**:
- `mapped_by`: "auto" (from Gong metadata) or "manual" (human-created)
- `mapped_date`: When this mapping was established

### Creating Manual Mappings

When to create manual mappings:
- Gong calls don't have Salesforce IDs in metadata
- You're using multiple CRMs (e.g., migrated from HubSpot to Salesforce)
- Account names don't match between systems

**Process**:
1. Export unmatched records
2. Use fuzzy matching or manual review
3. Store in `source/joins/mappings/system1_to_system2.csv`
4. Update `source/joins/keys.md` to document the mapping

## Troubleshooting Join Issues

### Problem: Transcripts aren't linking to opportunities

**Check**:
1. Does `source/transcripts/normalized/transcripts.parquet` have `opportunity_id`?
2. Are the opportunity IDs 15-char (Salesforce) or 18-char (API)?
   - Convert if needed: 15-char IDs are case-sensitive substrings of 18-char
3. Are there calls before the opportunity was created?
   - You may need to join by account + date range

### Problem: Enrichment data won't join to accounts

**Check**:
1. Compare `account_name` formats (legal name vs. trade name)
2. Try joining on `domain` field if available
3. Use fuzzy matching library (e.g., `fuzzywuzzy` in Python)
4. Create manual mapping table for top accounts

### Problem: Duplicate joins (1-to-many relationships)

**Example**: One opportunity has multiple calls.

**Solution**: Decide your grain of analysis:
- Analysis by **call**: Keep duplicates, one row per call
- Analysis by **opportunity**: Aggregate calls first
  ```sql
  SELECT
      opportunity_id,
      COUNT(*) as num_calls,
      MAX(call_date) as last_call_date
  FROM transcripts
  GROUP BY opportunity_id
  ```

## Join Key Documentation: `source/joins/keys.md`

Keep a summary of all active join keys in `source/joins/keys.md`:

```markdown
## Active Join Keys

- **CRM → Enrichment**: `account_name` (fuzzy) or `domain` (exact)
- **CRM → Transcripts**: `opportunity_id` (exact)
- **CRM → Personas**: `email_hash` (exact)
- **Enrichment → Transcripts**: Via CRM (account_id)
```

Update this file whenever you add a new data source.

---

**Golden Rule**: If you can't join two datasets, you can't answer cross-functional questions. Invest in clean join keys early.
