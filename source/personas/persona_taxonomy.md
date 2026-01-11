# Persona Taxonomy

<!--
PURPOSE: Define the types of people involved in your sales process.
This lets you tailor messaging and understand buying committee dynamics.

HOW TO USE:
- Label contacts in your CRM with these personas
- Reference when planning campaign messaging (different message per persona)
- Use in transcript analysis to understand who said what

WHAT TO FILL IN:
- Add your specific persona definitions
- Include job titles that map to each persona
- Document what each persona cares about and how to message them
-->

## Persona Types

### Champion 🏆
**Definition**: The internal advocate who wants your solution to win.

**Characteristics**:
- Will do work to get you in front of decision-makers
- Sees personal benefit from your product succeeding
- Has influence (even if not authority)
- Engages frequently, asks good questions

**Common Job Titles**:
- _[Example: Senior Engineer, DevOps Lead, Engineering Manager, Technical Lead]_

**What They Care About**:
- _[Example: Making their job easier, looking good to their team, getting promoted]_
- _[Example: Technical elegance, reducing toil, learning new skills]_

**How to Message Them**:
- _[Example: Show how they'll be the hero who fixed a painful problem]_
- _[Example: Emphasize time saved and technical quality]_
- _[Example: Provide assets they can use internally (one-pagers, ROI calculators)]_

**Red Flags (Not Actually a Champion)**:
- _[Example: Won't introduce you to their boss]_
- _[Example: Doesn't respond for weeks at a time]_
- _[Example: "I'll think about it" but never follows up]_

---

### Economic Buyer 💰
**Definition**: The person who controls the budget and makes final purchasing decision.

**Characteristics**:
- Has authority to approve spend
- Cares about business impact > technical details
- Often delegated evaluation to technical buyers
- Time-constrained, wants the bottom line

**Common Job Titles**:
- _[Example: VP Engineering, CTO, Director of Engineering, Head of DevOps]_

**What They Care About**:
- _[Example: ROI, risk mitigation, team productivity]_
- _[Example: Cost compared to alternatives (including doing nothing)]_
- _[Example: "Will this help us ship faster / reduce costs / avoid outages?"]_

**How to Message Them**:
- _[Example: Lead with business outcomes, not features]_
- _[Example: Show ROI calculation (time saved × cost of engineer time)]_
- _[Example: Risk: "Cost of one outage > annual cost of our platform"]_

**Questions They Ask**:
- _[Example: "How much does this cost?"]_
- _[Example: "What's the implementation timeline?"]_
- _[Example: "What if we do nothing?"]_

---

### Technical Buyer 🔍
**Definition**: The gatekeeper who must approve from security/compliance/architecture perspective.

**Characteristics**:
- Can say "no" but often can't say "yes"
- Detail-oriented, risk-averse
- Needs documentation and proof
- Often in Security, Compliance, Enterprise Architecture

**Common Job Titles**:
- _[Example: Security Engineer, Compliance Manager, Enterprise Architect, CISO]_

**What They Care About**:
- _[Example: Security, compliance, data privacy]_
- _[Example: Integration with existing stack]_
- _[Example: Vendor risk (will you go out of business?)]_

**How to Message Them**:
- _[Example: Provide security documentation upfront]_
- _[Example: Show compliance certifications (SOC 2, GDPR, etc.)]_
- _[Example: Explain architecture, data flow, access controls]_

**Questions They Ask**:
- _[Example: "How is data encrypted?"]_
- _[Example: "What's your SLA?"]_
- _[Example: "Can we self-host?"]_

**How to Accelerate**:
- _[Example: Offer a security review call]_
- _[Example: Share a "Security FAQ" document]_
- _[Example: Connect them with your security team directly]_

---

### Blocker 🚫
**Definition**: Someone who will actively work against your solution.

**Characteristics**:
- Opposes your solution for technical, political, or personal reasons
- May have built internal tool you're replacing
- May prefer a competitor
- Can derail deals if not addressed

**Common Job Titles**:
- _[Any role, but often someone who built the current solution or has strong opinion about alternatives]_

**What They Care About** (Why They Block):
- _[Example: "Not invented here" - they built current solution]_
- _[Example: Job security - worried you'll make them redundant]_
- _[Example: Prefer a competitor - already committed to another vendor]_

**How to Handle Them**:
- _[Example: Understand their objection - is it technical, political, or personal?]_
- _[Example: If technical: Address with data and proof]_
- _[Example: If political: Work around them via champion]_
- _[Example: If personal: Acknowledge their contribution, position as evolution not replacement]_

**When to Give Up**:
- _[Example: If they're the economic buyer and actively opposed, deal is likely dead]_

---

### End User 👤
**Definition**: The person who will actually use your product day-to-day.

**Characteristics**:
- Not involved in buying decision
- Adoption success depends on them
- May not know evaluation is happening
- Care about usability, not business case

**Common Job Titles**:
- _[Example: Software Engineer, Frontend Developer, Full-Stack Engineer]_

**What They Care About**:
- _[Example: Is it easy to use?]_
- _[Example: Does it fit my workflow?]_
- _[Example: Will it make my job easier or harder?]_

**How to Message Them** (if you get to):
- _[Example: Show, don't tell - live demo or trial]_
- _[Example: Emphasize ease of use and learning curve]_
- _[Example: "You'll be productive in 15 minutes"]_

**Why They Matter**:
- _[Example: If end users hate it, champion can't get adoption]_
- _[Example: Low adoption = churn]_

---

### Influencer 🎤
**Definition**: Someone whose opinion carries weight, but doesn't have authority or budget.

**Characteristics**:
- Consulted by decision-makers
- Often senior IC or trusted advisor
- Can accelerate or slow down deals
- Not formally part of buying committee

**Common Job Titles**:
- _[Example: Staff Engineer, Principal Engineer, Senior Architect, Advisor]_

**What They Care About**:
- _[Example: Technical quality, long-term implications]_
- _[Example: "Is this the right architectural decision?"]_

**How to Message Them**:
- _[Example: Deep technical content, architecture discussions]_
- _[Example: Show thought leadership (blog posts, talks)]_

---

## Persona Labeling in Practice

### In Your CRM
Add a custom field `persona_label` to contacts:
- Champion
- Economic Buyer
- Technical Buyer
- Blocker
- End User
- Influencer
- Unknown (not yet determined)

### In Transcripts
When analyzing calls, tag who said what:
```json
{
  "speaker": "Champion",
  "quote": "We've been trying to solve this for 6 months..."
}
```

### In Campaigns
Target messaging by persona:

| Persona | Email Subject Line Example | Key Message |
|---------|----------------------------|-------------|
| Champion | _["How to pitch [Product] to your VP"]_ | _[Give them ammunition for internal advocacy]_ |
| Economic Buyer | _["3 ways [Product] pays for itself"]_ | _[ROI and business case]_ |
| Technical Buyer | _["Security review: [Product] architecture"]_ | _[Address their concerns upfront]_ |

See `prompts/messaging_generation.md` for templates per persona.

## Updating Persona Definitions

**When to update**:
- After discovering a new persona type in your sales process
- When buying committee structure changes (e.g., security becomes more involved)
- After win/loss analysis reveals persona patterns

**Process**:
1. Review transcripts and notice patterns
2. Document new persona or update existing
3. Update `source/personas/personas.yaml` with structured data
4. Retrain team and AI agents on new definitions

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name/Team]_
**Change Log**: _[What changed and why]_
