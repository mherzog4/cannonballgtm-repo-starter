# Privacy & Redaction Guidelines

<!--
PURPOSE: This file defines what data can be committed to this repo,
what must be redacted, and how to handle PII (Personally Identifiable Information).

HOW TO USE:
- Review this before committing CRM exports or transcripts
- Follow redaction scripts (in pipelines/) before git add
- Check this when sharing repo access with contractors or partners

WHEN TO UPDATE:
- When legal/compliance requirements change
- When adding new data sources with sensitive fields
- After a privacy incident (learn and document)
-->

## Privacy Tiers

### ✅ Tier 1: Always Safe (Can Commit Publicly)

These fields are anonymized or aggregated enough to be safe:

- **Industry** (e.g., "Financial Services")
- **Headcount ranges** (e.g., "500-1000")
- **Region** (e.g., "North America")
- **Job titles** (e.g., "VP of Engineering")
- **Seniority levels** (e.g., "VP")
- **Persona labels** (e.g., "Champion", "Blocker")
- **Tech stack** (e.g., ["Salesforce", "AWS"])
- **Deal amounts** (if account is anonymized)
- **Transcript themes** (extracted insights, not raw text)

### ⚠️  Tier 2: Requires Redaction (Can Commit After Processing)

These fields need transformation before committing:

- **Email addresses** → Hash with SHA256 → `email_hash`
- **Phone numbers** → Redact entirely or hash
- **Contact names** → Replace with `<Champion at Account_12345>`
- **Account names** → Replace with `Account_12345` (numbered)
- **Specific product names** → Replace with generic terms if under NDA
- **URLs with account identifiers** → Redact or replace with placeholder

### 🚫 Tier 3: Never Commit (Keep in Local/Secure Storage Only)

These should never be in version control:

- **API keys or credentials**
- **Raw PII** (unredacted names, emails, phone numbers)
- **Private Slack/email conversations** (unless consent given)
- **Internal financial projections** (unless repo is private and access-controlled)
- **Customer data under NDA**

## Redaction Scripts

### Email Hashing

**Before**:
```csv
contact_id,email,job_title
003ABC,john.doe@acme.com,VP Engineering
```

**After**:
```csv
contact_id,email_hash,job_title
003ABC,7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069,VP Engineering
```

**Script**: `pipelines/redact_emails.py`

```python
import hashlib
import pandas as pd

def redact_emails(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # Hash emails
    df['email_hash'] = df['email'].apply(
        lambda e: hashlib.sha256(e.lower().strip().encode()).hexdigest()
    )

    # Drop original email column
    df = df.drop(columns=['email'])

    df.to_csv(output_csv, index=False)
    print(f"Redacted {len(df)} emails → {output_csv}")
```

### Account Name Anonymization

**Before**:
```csv
account_id,account_name,industry,headcount
001XYZ,Acme Corporation,Financial Services,450
```

**After**:
```csv
account_id,account_label,industry,headcount
001XYZ,Account_001,Financial Services,450
```

**Script**: `pipelines/anonymize_accounts.py`

Create a mapping table (store securely, NOT in git):
```csv
account_id,account_name,account_label
001XYZ,Acme Corporation,Account_001
```

### Transcript Redaction

**Before**:
```json
{
  "transcript_id": "call_123",
  "transcript_text": "Hi, this is John from Acme Corporation. Our CEO Sarah mentioned..."
}
```

**After**:
```json
{
  "transcript_id": "call_123",
  "transcript_text": "Hi, this is <Champion> from <Account_001>. Our <CEO> mentioned..."
}
```

**Tools**:
- **Named Entity Recognition (NER)**: Use spaCy or AWS Comprehend to detect person names
- **Regex patterns**: Detect emails, phone numbers, URLs
- **Manual review**: For sensitive transcripts, human review is safest

## Workflow for Committing Sensitive Data

### Step 1: Export Raw Data
```bash
# Export from Salesforce, Gong, etc.
# Store in source/*/raw/ (NOT committed to git yet)
```

### Step 2: Run Redaction Pipeline
```bash
python pipelines/redact_crm_data.py \
  --input source/crm/exports/raw/crm_contacts_2026-01-10.csv \
  --output source/crm/exports/crm_contacts_2026-01-10.csv \
  --mapping-output .local/account_mapping_2026-01-10.csv  # Store securely
```

### Step 3: Review Output
- Spot-check redacted files for PII leakage
- Search for `@` (emails), `xxx-xxx-xxxx` (phones), proper nouns

### Step 4: Commit Redacted Data
```bash
git add source/crm/exports/crm_contacts_2026-01-10.csv
git commit -m "Add redacted CRM contacts export (2026-01-10)"
```

### Step 5: Store Mapping Securely
The mapping file (e.g., `account_mapping_2026-01-10.csv`) should be stored:
- In a password-protected 1Password vault
- On an encrypted drive (not in git)
- In a private S3 bucket with IAM restrictions

**Why keep the mapping?** So you can de-anonymize data when needed for internal use.

## .gitignore Rules

Add these to your `.gitignore`:

```gitignore
# Raw, unredacted data
source/*/raw/
**/*_unredacted.csv
**/*_raw.csv

# Mapping files (never commit)
.local/
**/mappings/*_mapping.csv

# API keys and credentials
.env
.env.local
**/*.pem
**/*.key

# Database exports with PII
*.db
*.sqlite
```

## Legal Considerations

### GDPR (Europe)
- **Right to be forgotten**: If a contact requests deletion, remove from repo and history
- **Data minimization**: Only store fields you actually use
- **Consent**: If sharing transcripts, ensure call participants consented

### CCPA (California)
- **Right to know**: Document what data you store about California residents
- **Right to delete**: Be able to identify and remove individual records

### SOC 2 / HIPAA
- If your data is subject to compliance frameworks:
  - Consider making this repo **private** (not public)
  - Use branch protection and audit logs
  - Encrypt data at rest (use Git LFS with encryption)

## Incident Response

**If PII is accidentally committed:**

1. **Immediate**: Make repo private if it was public
2. **Remove from history**:
   ```bash
   git filter-branch --tree-filter 'rm -f path/to/file' HEAD
   git push --force
   ```
   (Or use `git filter-repo` for large repos)
3. **Notify affected parties** if legally required
4. **Update this doc** with lessons learned

## Sharing Repo Access

### Internal Team
- Full access to redacted data
- Access to mapping files (via secure channel)

### Contractors / Agencies
- Access to redacted data only
- No mapping files
- Sign NDA before repo access

### Public / Open Source
- Only Tier 1 data (see above)
- No account names, no emails, no raw transcripts
- Consider using synthetic data for examples

## Synthetic Data for Examples

For documentation and tutorials, create synthetic data:

```python
# Example: Generate fake accounts
import faker
fake = faker.Faker()

accounts = [
    {
        "account_id": f"00100000{i:06d}AAA",
        "account_label": f"Account_{i:03d}",
        "industry": fake.random_element(["SaaS", "Fintech", "Healthcare"]),
        "headcount": fake.random_int(min=50, max=2000),
    }
    for i in range(100)
]
```

This lets you demonstrate workflows without exposing real customer data.

---

**Golden Rule**: When in doubt, redact. It's easier to add data later than to remove it from git history.
