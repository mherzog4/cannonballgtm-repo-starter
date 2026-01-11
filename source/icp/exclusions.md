# ICP Exclusions

<!--
PURPOSE: Document who you DON'T sell to and why.
This prevents wasted effort on bad-fit prospects.

HOW TO USE:
- Reference when qualifying inbound leads
- Use to filter out accounts in campaign targeting
- Update when you discover new patterns of bad fits

WHAT TO FILL IN:
- Add specific exclusion criteria based on your experience
- Include the "why" so future team members understand the reasoning
- Update this after losing deals due to misfit
-->

## Company-Level Exclusions

### Too Small
- **Criteria**: _[Example: <10 employees, <$1M revenue]_
- **Why Exclude**: _[Example: Use case not acute enough, no budget, high churn risk]_
- **Exception**: _[Example: If they're very high-growth (50%+ MoM) and just raised funding]_

### Too Large
- **Criteria**: _[Example: >5,000 employees, enterprise-only buyers]_
- **Why Exclude**: _[Example: Sales cycle >12 months, need features we don't have, require enterprise SLAs]_
- **Exception**: _[Example: If they have a specific team/division that's our target size and can buy independently]_

### Wrong Industry
- **Industries**: _[Example: Government/Public Sector, Non-profit, Education]_
- **Why Exclude**: _[Example: Procurement process too complex, budget cycles too long, compliance requirements we don't meet]_
- **Exception**: _[Example: If they operate like a commercial business (e.g., private university with tech team)]_

### Geographic
- **Regions**: _[Example: Countries where we don't have data residency, non-English speaking markets]_
- **Why Exclude**: _[Example: Can't support local language, data sovereignty requirements, no payment methods]_
- **Exception**: _[Example: If they have English-speaking team and can use US/EU data centers]_

## Use Case Exclusions

### Not Cloud-Native
- **Criteria**: _[Example: Still entirely on-premise, no cloud migration plans]_
- **Why Exclude**: _[Example: Our product is cloud-only, they're not ready for our model]_

### Wrong Use Case
- **Use Cases We Don't Serve**:
  - _[Example: Looking for managed services (we're self-service)]_
  - _[Example: Need white-label/OEM (we don't offer that)]_
  - _[Example: Need on-premise deployment (cloud-only)]_
- **Why Exclude**: _[Example: Not our core offering, would require custom development]_

### Services-First Mindset
- **Criteria**: _[Example: "Can you do it for us?", "Need consulting hours", "Want managed service"]_
- **Why Exclude**: _[Example: We're a product company, don't have services org, margins don't work]_
- **Exception**: _[Example: If they'll use product for 80% and just need onboarding help]_

## Behavioral Red Flags

### Tire Kickers
- **Signs**: _[Example: "Just exploring", no timeline, no budget identified, won't engage champion]_
- **Why Exclude**: _[Example: Won't convert, wastes sales time]_
- **How to Spot**: _[Example: Won't answer budget/timing questions, no use case defined]_

### Wrong Buying Committee
- **Signs**: _[Example: Only end users engaged, no executive sponsor, no economic buyer access]_
- **Why Exclude**: _[Example: Can't get deal across the line without exec buy-in]_

### Unrealistic Expectations
- **Signs**: _[Example: "Need this feature we don't have", "Must be on-premise", "Need 99.999% SLA"]_
- **Why Exclude**: _[Example: We can't meet their requirements, will churn after buying]_

## Competitive Situations

### Locked Into Competitor
- **Criteria**: _[Example: Multi-year contract with competitor, just renewed]_
- **Why Exclude**: _[Example: No switching window for 1-2 years]_
- **Exception**: _[Example: If they're very unhappy and willing to pay exit fee]_

### Requires Features We Won't Build
- **Examples**:
  - _[Example: On-premise deployment (we're cloud-only by design)]_
  - _[Example: SOC 2 Type II (we're not there yet)]_
  - _[Example: 24/7 phone support (we don't offer this tier)]_
- **Why Exclude**: _[Example: Strategic decision not to build these, would distract from core]_

## How to Handle Exclusions in Practice

### For Inbound Leads
1. Score against ICP (see `source/icp/icp.md`)
2. Check exclusion criteria
3. If match, route to disqualification flow:
   - "Thanks for your interest. Based on [X], we're not a great fit because [Y]."
   - Point them to alternative solutions if helpful

### For Outbound Campaigns
1. Filter out exclusions in `campaigns/*/segment.yaml`
2. Use negative filters in `pipelines/campaign_pull.py`:
   ```python
   # Exclude companies < 50 employees
   df = df[df['headcount'] >= 50]

   # Exclude certain industries
   excluded_industries = ['Government', 'Non-profit']
   df = df[~df['industry'].isin(excluded_industries)]
   ```

### Tracking Exclusions
Log why accounts were excluded in `analysis/segmentation/exclusions_log.csv`:

| account_id | exclusion_reason | date | notes |
|------------|------------------|------|-------|
| 001ABC | Too small (<10 employees) | 2026-01-10 | Seed stage, no budget |
| 002DEF | Wrong use case (services) | 2026-01-10 | Wanted consulting, not product |

This helps you learn what NOT to target over time.

## Updating These Exclusions

**When to update**:
- After losing a deal due to misfit (add that reason)
- After wasting time on bad leads (prevent in future)
- When product capabilities change (may remove exclusions)

**Process**:
1. Review lost deals in `analysis/win_loss/themes.md`
2. Identify patterns: "We keep losing to X type of company because Y"
3. Add to exclusions list
4. Update filtering logic in pipelines

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
**Change Log**: _[What changed and why]_
