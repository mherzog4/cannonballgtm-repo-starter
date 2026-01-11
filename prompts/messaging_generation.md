# Prompt: Campaign Messaging Generation

<!--
PURPOSE: Generate personalized campaign messaging based on segment, persona, and situational change.
Use this to create email sequences, talk tracks, and value props that actually resonate.

HOW TO USE:
1. Define your campaign target (segment + situational change)
2. Load relevant context (ICP, positioning, win themes, past customer examples)
3. Run this prompt to generate messaging
4. Review, edit, and deploy

THE GOAL:
Create messaging that's specific to THIS prospect's situation, not generic marketing.
-->

## Prompt Template

```
You are writing a campaign message for a sales outreach.

CAMPAIGN CONTEXT:
- Target Segment: [INSERT, e.g., "Mid-Market Fintech"]
- Situational Change: [INSERT, e.g., "Post-Series B Funding"]
- Target Persona: [INSERT, e.g., "VP Engineering"]
- Campaign Goal: [INSERT, e.g., "Book discovery call"]

COMPANY CONTEXT:

**Our ICP** (from source/icp/icp.md):
[PASTE RELEVANT ICP SECTION]

**Our Positioning** (from source/icp/positioning.md):
[PASTE POSITIONING FOR THIS PERSONA]

**Why We Win** (from analysis/win_loss/themes.md):
[PASTE TOP 3 WIN THEMES]

**Similar Customer Examples**:
- Customer A: [industry, headcount, what they achieved]
- Customer B: [industry, headcount, what they achieved]

TARGET PROSPECT:
- Company: [Company Name]
- Industry: [Industry]
- Headcount: [Number]
- Situational Change: [What just happened, e.g., "Raised $25M Series B 2 months ago"]
- Research Findings: [Any news, LinkedIn posts, job postings, etc.]

YOUR TASK:
Write a personalized outreach email that:

1. HOOKS with their situational change (not generic)
2. RELATES to their specific pain point (not "deployment" but "scaling infra post-funding")
3. PROVES with similar customer example (social proof from their segment)
4. CALLS TO ACTION clearly (what do you want them to do?)

STYLE:
- Conversational, not corporate
- Short (200-300 words MAX)
- Specific (mention their situation, not generic)
- Value-first (how you help, not what you are)

STRUCTURE:

**Subject Line**: [Personalized, mentions situational change]
- Example: "Congrats on the Series B, [Name]"
- Example: "[Company]'s infrastructure post-funding"

**Email Body**:

[Opening line - reference their situation]

[Problem statement - their likely pain right now]

[Social proof - customer like them who solved this]

[Call to action - clear next step]

[Signature]

---

EXAMPLES TO FOLLOW:

**Good Example (Specific)**:
> Subject: Infrastructure at scale post-Series B
>
> Hi [Name],
>
> Congrats on closing the Series B last month - saw the announcement on Crunchbase.
>
> Most fintech teams we work with hit a deployment bottleneck within 6 months of raising. Engineering team grows from 15 to 40, but deploy process is still manual from the 5-person days.
>
> [Similar Customer] had the same challenge post-Series B. They were spending 10+ hours/week babysitting deployments. Switched to [Product] and got that time back to ship features.
>
> Worth 15 minutes to show you how they did it?
>
> Best,
> [Name]

**Bad Example (Generic)**:
> Subject: Automate your deployments
>
> Hi [Name],
>
> Are you tired of manual deployments? [Product] can help!
>
> We offer deployment automation for modern engineering teams. Features include:
> - Automated CI/CD
> - Monitoring
> - Rollbacks
>
> Let's schedule a demo!

---

OUTPUT:

Generate 3 variations:
1. **Direct** (straight to the point, for busy exec)
2. **Story-driven** (opens with customer story, for engaged prospect)
3. **Problem-first** (leads with pain point, for awareness stage)

For each variation, provide:
- Subject line
- Email body
- Expected response rate (based on our data): [X%]
- When to use: [scenario]

```

## Input Data Preparation

```python
# Load campaign context
import yaml

# Load ICP
with open('source/icp/icp.md') as f:
    icp = f.read()

# Load positioning
with open('source/icp/positioning.md') as f:
    positioning = f.read()

# Load win themes
with open('analysis/win_loss/themes.md') as f:
    win_themes = f.read()

# Load campaign targets
targets = pd.read_csv('campaigns/2026-01-10_midmarket_fintech/pulled_customers.csv')

# For each target, generate personalized message
for _, row in targets.iterrows():
    prospect_context = f"""
    Company: {row['account_name']}
    Industry: {row['industry']}
    Headcount: {row['headcount']}
    Situational Change: {row['situational_change']}
    Research Findings: {row['research_notes']}
    """

    # Pass to AI with prompt template
    # ...
```

## Output Destination

Save generated messaging to:
- `campaigns/YYYY-MM-DD_name/assets/sequences/v1_email_1.md`
- `campaigns/YYYY-MM-DD_name/assets/sequences/v1_email_2.md`
- etc.

## Testing & Iteration

1. Deploy to small batch (20-50 prospects)
2. Measure response rate
3. If <5% response: Revise hook or social proof
4. If 10%+ response: Scale up
5. Document learnings in `campaigns/*/results/learnings.md`

---

**Version**: v1.0
**Last Updated**: _[YYYY-MM-DD]_
