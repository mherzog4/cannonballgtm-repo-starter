# Persona Labeling Guide

<!--
PURPOSE: Step-by-step instructions for labeling contacts with personas.
This can be done manually or with AI assistance.

HOW TO USE:
- Use this when you first set up the repo to label your CRM contacts
- Reference when training new team members on persona labeling
- Feed this guide to AI agents to have them auto-label personas

THE WORKFLOW:
1. Export your CRM contacts
2. Use this guide to label who's who
3. AI can help - describe what a "champion" looks like in your data
   (e.g., "frequent email engagement, introduced us to their boss")
4. Store labeled data in source/personas/persona_labels.csv
5. Join back to your CRM data via email_hash

WHY THIS MATTERS:
Knowing who's who lets you tailor messaging per persona and understand
buying committee dynamics. Without labels, all contacts look the same.
-->

## Quick Reference: Persona Identification

| Persona | Key Question | Positive Signal |
|---------|--------------|-----------------|
| **Champion** | Do they actively help us win? | Introduces you to decision-makers, asks "how can I help?", responds quickly |
| **Economic Buyer** | Do they control the budget? | Has VP/Director/C-level title, asks about pricing, mentions budget cycle |
| **Technical Buyer** | Do they gate on security/compliance? | Has security/compliance title, asks about certifications, wants architecture docs |
| **Blocker** | Do they oppose our solution? | Advocates for competitor, built internal tool, says "we don't need this" |
| **End User** | Will they use it day-to-day? | Individual contributor title, asks about workflow, wants to try it |
| **Influencer** | Does their opinion carry weight? | Staff/Principal title, consulted by others, asks deep technical questions |

## Step-by-Step Labeling Process

### Step 1: Export CRM Contacts

Export all contacts from your CRM with these fields:
- `contact_id`
- `email`
- `job_title`
- `account_id`
- `engagement_level` (e.g., how many emails/calls)

Save to: `source/crm/exports/crm_contacts_YYYY-MM-DD.csv`

### Step 2: Identify Champions (Start Here)

Champions are easiest to spot because they show up in your data as highly engaged.

**Look for contacts who**:
- Have multiple calls or emails with you
- Introduced you to their boss or other stakeholders
- Said things like "How can I help?" or "What do you need from me?"
- Responded within hours, not days

**Job Titles That Are Often Champions**:
- Senior Engineer
- DevOps Lead
- Engineering Manager
- Technical Lead

**In Transcripts, Champions Say**:
- "We've been trying to solve this for 6 months"
- "I love this, how do I get my boss on board?"
- "Let me set up a call with our VP"

**Action**: Label these contacts as `Champion` in your CSV.

### Step 3: Identify Economic Buyers

**Look for contacts who**:
- Have VP, Director, or C-level titles (VP Eng, CTO, etc.)
- Asked about pricing or budget
- Said "We need to fit this into Q2 budget"
- Final decision-makers on the deal

**Job Titles**:
- VP Engineering
- CTO
- Director of Engineering
- Head of [Department]

**In Transcripts, Economic Buyers Say**:
- "How much does this cost?"
- "What's the ROI?"
- "Can we start small and expand?"

**Action**: Label these contacts as `Economic Buyer` in your CSV.

### Step 4: Identify Technical Buyers

**Look for contacts who**:
- Have security, compliance, or architect titles
- Asked about SOC 2, GDPR, encryption, SLA
- Needed to approve before deal could proceed
- Often came into the process mid-way

**Job Titles**:
- Security Engineer
- Compliance Manager
- Enterprise Architect
- CISO

**In Transcripts, Technical Buyers Say**:
- "What's your data retention policy?"
- "Can we self-host?"
- "How is data encrypted in transit and at rest?"

**Action**: Label these contacts as `Technical Buyer` in your CSV.

### Step 5: Identify Blockers (Proceed with Caution)

**Look for contacts who**:
- Advocated for a competitor
- Built the internal tool you're replacing
- Consistently raised objections or went silent
- Said "We don't really need this"

**Warning**: Be careful labeling someone as a blocker. Sometimes they're just skeptical and need more info.

**In Transcripts, Blockers Say**:
- "Why not just use [competitor]?"
- "I built our current system and it works fine"
- "This seems unnecessary"

**Action**: Label as `Blocker` only if you're confident they actively opposed you.

### Step 6: Identify End Users and Influencers

**End Users**:
- Individual contributors who will use the product
- Often not involved in buying decision
- Job titles: Software Engineer, Developer

**Influencers**:
- Senior ICs (Staff, Principal Engineer)
- Consulted by decision-makers
- Opinion carries weight, but no budget authority

**Action**: Label remaining contacts as `End User`, `Influencer`, or `Unknown`.

## Using AI to Auto-Label Personas

You can ask AI (Claude Code, ChatGPT, etc.) to help label personas:

### Example Prompt for AI Labeling

```
I have a CSV of CRM contacts with these columns: contact_id, email, job_title, engagement_level, notes.

I need to label each contact with a persona: Champion, Economic Buyer, Technical Buyer, Blocker, End User, Influencer, or Unknown.

Here's how to identify each persona:
- Champion: Highly engaged, introduced us to others, helps us win. Often Senior Engineer, Engineering Manager.
- Economic Buyer: VP, Director, or C-level. Controls budget. Asks about pricing.
- Technical Buyer: Security, Compliance, Architect. Gates on security/compliance. Asks about certifications.
- Blocker: Actively opposes our solution. Says "we don't need this" or prefers competitor.
- End User: Individual contributor who will use product day-to-day. Software Engineer, Developer.
- Influencer: Staff/Principal Engineer. Opinion carries weight but no formal authority.

Here's a sample of my data:
[paste 10 rows of your CSV]

Please label the persona column for each row. If unsure, use "Unknown".
```

**Output**: AI will return a labeled CSV. Review it for accuracy before using.

## Storing Labeled Personas

### File Format: `source/personas/persona_labels.csv`

| contact_id | email_hash | persona_label | confidence | labeled_by | labeled_date |
|------------|------------|---------------|------------|------------|--------------|
| 003ABC | 7f83b165... | Champion | high | manual | 2026-01-10 |
| 003DEF | 8g94c276... | Economic Buyer | high | ai | 2026-01-10 |
| 003GHI | 9h05d387... | Unknown | low | ai | 2026-01-10 |

**Columns**:
- `contact_id`: From your CRM
- `email_hash`: SHA256 hash of email (for privacy-safe joins)
- `persona_label`: One of the persona types
- `confidence`: `high`, `medium`, `low` (how sure are you?)
- `labeled_by`: `manual` (human) or `ai` (automated)
- `labeled_date`: When this was labeled

### Why Use email_hash Instead of Email?

**Privacy**: If you share this repo, you don't expose real emails.
**Joining**: You can still join to other datasets using email_hash.

**How to hash**:
```python
import hashlib
email_hash = hashlib.sha256(email.lower().strip().encode()).hexdigest()
```

## Joining Personas Back to CRM Data

Once you have `persona_labels.csv`, join it back to your CRM exports:

```python
import pandas as pd

# Load CRM contacts
contacts = pd.read_csv('source/crm/exports/crm_contacts_2026-01-10.csv')

# Hash emails
contacts['email_hash'] = contacts['email'].apply(
    lambda e: hashlib.sha256(e.lower().strip().encode()).hexdigest()
)

# Load persona labels
personas = pd.read_csv('source/personas/persona_labels.csv')

# Join
enriched = contacts.merge(personas, on='email_hash', how='left')

# Now you have persona_label column on all contacts
print(enriched[['contact_id', 'job_title', 'persona_label']].head())
```

## Common Challenges

### Challenge: Contact Hasn't Engaged Yet
**Solution**: Label as `Unknown` until you have more data.

### Challenge: Contact Seems Like Multiple Personas
**Example**: A VP who's also very technical and acts like a champion.
**Solution**: Pick the **primary role** they play in your deal. If they control budget, they're `Economic Buyer` even if they're technical.

### Challenge: Persona Changes Over Time
**Example**: Champion gets promoted to VP and becomes Economic Buyer.
**Solution**: Update the label. Keep historical labels if you want to track changes:

| contact_id | persona_label | start_date | end_date |
|------------|---------------|------------|----------|
| 003ABC | Champion | 2025-01-01 | 2025-12-31 |
| 003ABC | Economic Buyer | 2026-01-01 | NULL |

## Improving Labels Over Time

**After each campaign**:
1. Review who actually helped you win (were they labeled Champion?)
2. Update labels if you got it wrong
3. AI can help refine: "Here's who we thought were champions vs. who actually were. What patterns do you see?"

**After reviewing transcripts**:
1. Search for phrases like "I'll introduce you to..." (Champion behavior)
2. Search for "How much does this cost?" (Economic Buyer behavior)
3. Update labels based on what they said

## Validation

**Spot-check your labels**:
- Do 80%+ of `Champion` labels have high engagement?
- Do 80%+ of `Economic Buyer` labels have VP/Director titles?
- Do `Blocker` labels make sense (are they actually opposing you)?

If not, revise your labeling criteria.

---

**Golden Rule**: When in doubt, label as `Unknown`. It's better to be honest about uncertainty than to mislabel and make bad decisions based on wrong data.

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
