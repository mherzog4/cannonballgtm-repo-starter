# Data Dictionary

<!--
PURPOSE: This file documents all data fields across your GTM repository.
When a new team member joins or an AI assistant analyzes your data,
they should refer here to understand what each column means.

HOW TO USE:
- Add new fields as you ingest new data sources
- Include data type, example values, and source system
- Document any transformations or business logic
- Keep this updated as your schema evolves

WHEN TO UPDATE:
- After ingesting new CRM exports
- When adding new enrichment fields
- After normalizing transcripts with new metadata
-->

## Core Business Entities

### Account
The company/organization that could buy from you.

| Field | Type | Description | Example | Source |
|-------|------|-------------|---------|--------|
| `account_id` | string | Unique identifier (usually from CRM) | `"0011234567ABCDE"` | Salesforce |
| `account_name` | string | Legal or common company name | `"Acme Corp"` | Salesforce |
| `industry` | string | Industry classification | `"Financial Services"` | Clay/Clearbit |
| `headcount` | integer | Number of employees | `450` | Clay/Clearbit |
| `arr` | decimal | Annual recurring revenue from this account | `24000.00` | Salesforce (derived) |
| `segment` | string | SMB / Mid-Market / Enterprise | `"Mid-Market"` | Derived (see segmentation rules) |
| `region` | string | Geographic region | `"North America"` | Salesforce |

### Contact
Individual person at an account.

| Field | Type | Description | Example | Source |
|-------|------|-------------|---------|--------|
| `contact_id` | string | Unique identifier | `"0031234567ABCDE"` | Salesforce |
| `email_hash` | string | Hashed email for privacy-safe joins | `"7f83b1657..."` | Derived (SHA256) |
| `job_title` | string | Current role | `"VP of Engineering"` | Salesforce |
| `persona_label` | string | Champion / Blocker / Economic Buyer / Technical Buyer | `"Champion"` | Manually labeled |
| `seniority` | string | Individual Contributor / Manager / Director / VP / C-Level | `"VP"` | Enrichment |

### Opportunity
A sales opportunity/deal in your CRM.

| Field | Type | Description | Example | Source |
|-------|------|-------------|---------|--------|
| `opportunity_id` | string | Unique identifier | `"0061234567ABCDE"` | Salesforce |
| `account_id` | string | Foreign key to Account | `"0011234567ABCDE"` | Salesforce |
| `stage` | string | Current deal stage | `"Proposal"` | Salesforce |
| `close_date` | date | Expected or actual close date | `"2026-01-15"` | Salesforce |
| `amount` | decimal | Deal value | `24000.00` | Salesforce |
| `is_won` | boolean | Did we win this deal? | `true` | Salesforce |
| `is_closed` | boolean | Is this deal closed (won or lost)? | `true` | Salesforce |

### Transcript
A recorded sales call (from Gong, Chorus, etc.).

| Field | Type | Description | Example | Source |
|-------|------|-------------|---------|--------|
| `transcript_id` | string | Unique identifier | `"call_789456123"` | Gong |
| `opportunity_id` | string | Linked opportunity (if available) | `"0061234567ABCDE"` | Gong metadata |
| `call_date` | datetime | When the call happened | `"2026-01-05T14:30:00Z"` | Gong |
| `duration_seconds` | integer | Call length | `1847` | Gong |
| `transcript_text` | text | Full transcript content | `"Thanks for joining..."` | Gong |
| `speakers` | array | List of speaker labels | `["Rep", "Champion", "Technical Buyer"]` | Gong (or derived) |
| `sentiment` | string | Overall sentiment | `"Positive"` | Gong or derived |

## Enrichment Fields

These come from external data providers (Clay, Clearbit, ZoomInfo):

| Field | Type | Description | Example | Source |
|-------|------|-------------|---------|--------|
| `tech_stack` | array | Technologies used | `["Salesforce", "AWS", "React"]` | BuiltWith/Clay |
| `funding_stage` | string | Startup funding stage | `"Series B"` | Crunchbase |
| `funding_amount` | decimal | Total funding raised | `25000000.00` | Crunchbase |
| `employee_growth_6mo` | decimal | % employee growth (6 months) | `0.23` | LinkedIn/Clay |
| `recent_news` | text | Recent news headlines | `"Acme Corp raises $25M..."` | Google News API |

## Derived Fields

Fields you compute from source data:

| Field | Type | Description | Calculation | Use Case |
|-------|------|-------------|-------------|----------|
| `segment` | string | Company size bucket | Based on `headcount` (see `analysis/segmentation/segment_rules.yaml`) | Campaign targeting |
| `is_champion_engaged` | boolean | Has a champion persona engaged? | Count of calls with champion persona > 0 | Deal health scoring |
| `days_in_stage` | integer | Days in current stage | `today - stage_change_date` | Pipeline velocity |
| `situational_change` | string | Trigger that caused interest | Extracted from transcripts (see `prompts/situational_change_extraction.md`) | Messaging personalization |

## Privacy & Redaction

**Fields that should be redacted before public sharing:**
- `email` → Replace with `email_hash`
- `phone_number` → Redact entirely or hash
- `contact_name` → Replace with persona label + account name
- Specific product names (if under NDA)

**Fields that are safe to share:**
- Industry, headcount, region (aggregated)
- Job titles, seniority levels
- Deal stages, amounts (if anonymized)

See `docs/privacy_and_redaction.md` for full guidelines.

## Adding New Fields

When you add a new field:
1. Document it in this file with type, description, example, and source
2. Update relevant schema files in `source/*/schemas/`
3. Update join key documentation if it's a new identifier
4. Consider if it should be redacted (update privacy doc)

---

**Keep this living document updated**. If an AI or human can't understand your data, they can't help you use it effectively.
