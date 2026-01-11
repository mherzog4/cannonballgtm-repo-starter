# Ideal Customer Profile (ICP)

<!--
PURPOSE: Define who you sell to, how you win, and what makes a great fit.
This is your "target market" definition that should inform all campaigns.

HOW TO USE:
- Reference this when building segments in analysis/segmentation/
- Update quarterly based on win/loss analysis
- Use this to score new leads ("How well do they match our ICP?")

WHAT TO FILL IN:
- Replace placeholder examples with your actual ICP criteria
- Be specific (not "SaaS companies" but "B2B SaaS, post-Series A, 50-200 employees")
- Include both firmographic (company) and behavioral (what they do) traits
-->

## Core ICP Definition

### Who We Sell To

**Company Profile**:
- **Industry**: _[Example: B2B SaaS, Fintech, Healthcare IT]_
- **Company Stage**: _[Example: Post-Series A, Profitable, Scale-up]_
- **Headcount**: _[Example: 50 to 500 employees]_
- **Revenue**: _[Example: $5M to $50M ARR]_
- **Geography**: _[Example: North America, English-speaking markets]_

**Use Case Profile**:
- **Primary Use Case**: _[Example: Engineering teams managing infrastructure at scale]_
- **Pain Point We Solve**: _[Example: Manual deployment processes, lack of observability, high error rates]_
- **Alternative They're Using**: _[Example: Jenkins + manual scripts, GitHub Actions, internal tools]_
- **Why They Outgrow It**: _[Example: Doesn't scale, lacks collaboration features, too brittle]_

### Firmographic Indicators

These are signals that a company is likely a good fit:

| Indicator | Why It Matters |
|-----------|----------------|
| _[Example: 10+ engineers]_ | _[Need is acute at this scale]_ |
| _[Example: Raised funding in last 12 months]_ | _[Budget available, growth mindset]_ |
| _[Example: Using AWS/GCP/Azure]_ | _[Already cloud-native, technical buyer present]_ |
| _[Example: Posted job for DevOps/SRE role]_ | _[Hiring indicates pain point]_ |

### Behavioral Indicators

These are actions/events that suggest timing is right:

| Trigger Event | Why It's a Good Time to Reach Out |
|---------------|-------------------------------------|
| _[Example: Outage or downtime mentioned in news]_ | _[Acute pain, looking for solutions]_ |
| _[Example: New VP of Engineering joined]_ | _[New leader wants to make an impact]_ |
| _[Example: Announcing new product line]_ | _[Need to scale infrastructure]_ |
| _[Example: Migrating from on-prem to cloud]_ | _[Re-evaluating tooling]_ |

## How We Win

### Our Unique Advantage

_[Example: We're the only solution that combines X with Y, making it 10x faster to achieve Z without needing a dedicated team.]_

### Why Customers Choose Us

Based on `analysis/win_loss/differentiators.md`:

1. **[Differentiator 1]**: _[Example: Time to value - get up and running in <1 hour]_
2. **[Differentiator 2]**: _[Example: Collaboration features - whole team can contribute]_
3. **[Differentiator 3]**: _[Example: Pricing model - aligns with their usage, not seat count]_

### Common Buying Committee

| Role | Persona | Influence |
|------|---------|-----------|
| **Champion** | _[Example: Senior Engineer or DevOps Lead]_ | Drives evaluation, builds internal case |
| **Economic Buyer** | _[Example: VP Engineering or CTO]_ | Approves budget |
| **Technical Buyer** | _[Example: Security/Compliance team]_ | Must approve for security/compliance |
| **End Users** | _[Example: Software Engineers]_ | Adoption success depends on them |

See `source/personas/personas.yaml` for detailed persona definitions.

## Red Flags (Exclusions)

These indicate a company is **NOT** a good fit:

| Red Flag | Why We Exclude |
|----------|----------------|
| _[Example: <10 employees]_ | _[Use case not acute yet, low budget]_ |
| _[Example: Still on-premise only]_ | _[Not ready for cloud-native tooling]_ |
| _[Example: Enterprise with 10k+ employees]_ | _[Sales cycle too long, need enterprise features we don't have]_ |
| _[Example: Looking for services/consulting]_ | _[We're a product company, not services]_ |

See `source/icp/exclusions.md` for full list.

## ICP Scoring (Optional)

You can score accounts based on ICP fit:

| Criteria | Score |
|----------|-------|
| Industry match | 0-20 pts |
| Headcount in range | 0-20 pts |
| Funding/revenue signal | 0-20 pts |
| Behavioral trigger present | 0-20 pts |
| Champion persona identified | 0-20 pts |

**Total**: 0-100 pts
- **80-100**: Hot lead, prioritize
- **60-79**: Good fit, include in campaigns
- **40-59**: Maybe, if strong situational trigger
- **<40**: Likely not a fit

## Updating This ICP

**When to update**:
- After quarterly win/loss review
- When entering new market segment
- When product positioning changes

**Process**:
1. Review `analysis/win_loss/themes.md`
2. Identify patterns in who we win vs. lose
3. Update criteria above
4. Test new ICP definition in next campaign
5. Measure conversion rates before/after

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
**Change Log**: _[What changed and why]_
