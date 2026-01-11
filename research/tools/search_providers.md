# Research Tools & Search Providers

<!--
PURPOSE: Document tools for researching prospects and finding situational triggers.
These help you find publicly visible signals (funding, news, job postings, outages).

HOW TO USE:
- Reference when building research pipelines
- Update with new tools as you discover them
- Track costs to stay within budget
-->

## Web Search APIs

### Serp.dev

**What It Does**: Google Search API with structured results

**Use Cases**:
- Find funding announcements: "fintech series B 2025"
- Find news about companies: "[company name] news"
- Find outages: "[company name] down"

**Pricing**: $X per 1,000 searches

**API Docs**: https://serpapi.com/

**Example**:
```python
import requests

params = {
  "engine": "google",
  "q": "fintech series B funding 2025",
  "api_key": "YOUR_API_KEY"
}

response = requests.get("https://serpapi.com/search", params=params)
results = response.json()

# Save results
with open('research/snapshots/2026-01-15/serp_results.jsonl', 'a') as f:
    f.write(json.dumps(results) + '\n')
```

---

### OpenWebNinja (Budget Alternative)

**What It Does**: Web scraping + search at low cost

**Use Cases**:
- Similar to Serp.dev but cheaper
- Good for high-volume research

**Pricing**: $X per month (cheaper than Serp.dev)

**Recommended By**: [Attribution removed per user request]

---

## News & Press Release Monitoring

### Google News API

**What It Does**: Search news articles

**Use Cases**:
- Find funding announcements
- Find executive hires
- Find product launches
- Find outages or incidents

**Example Query**: "[company name] raises series B"

---

### NewsAPI.org

**What It Does**: Aggregates news from multiple sources

**Pricing**: Free tier available, $X for commercial

**API Docs**: https://newsapi.org/docs

---

## Funding & Company Data

### Crunchbase API

**What It Does**: Funding rounds, investor data, company metadata

**Use Cases**:
- Find recent Series B/C fundings
- Track investor activity
- Company headcount and growth

**Pricing**: $X/month for API access

**Example**:
```python
# Find fintech companies that raised Series B in last 6 months
# (requires Crunchbase API key)
```

---

### LinkedIn Sales Navigator

**What It Does**: Advanced LinkedIn search and alerts

**Use Cases**:
- Find new VPs/CTOs (executive changes)
- Job posting alerts (hiring surge)
- Company growth metrics

**Pricing**: $X/month per seat

**Why It's Worth It**:
- "New VP Engineering" is a strong buying trigger
- Job postings = acknowledged need

---

## Tech Stack & Web Presence

### BuiltWith

**What It Does**: Detect technologies used on websites

**Use Cases**:
- Is company cloud-native? (AWS/GCP indicator)
- What tools do they already use?
- Tech stack sophistication

**Pricing**: $X/month for API

---

### Wappalyzer (Alternative)

**What It Does**: Similar to BuiltWith, detect web technologies

**Pricing**: Free browser extension, paid API

---

## Social Monitoring

### Twitter/X API

**What It Does**: Monitor mentions, track keywords

**Use Cases**:
- Find outages: "[company name] down"
- Customer complaints
- Product launches

**Pricing**: Free tier limited, $X/month for higher volume

---

### Reddit Monitoring

**What It Does**: Track mentions in relevant subreddits

**Use Cases**:
- Engineering teams discussing pain points
- Tool comparisons
- Community sentiment

**Tools**: Manual search or use Pushshift API

---

## Batch Processing

### Claude Code Batch API

**What It Does**: Process large volumes of data with AI

**Use Cases**:
- Analyze 100+ search results to find patterns
- Extract situational changes from news articles
- Classify companies by segment

**Pricing**: Cheaper than real-time API

**Example Workflow**:
1. Use Serp.dev to get search results
2. Save to JSONL file
3. Upload to Claude batch API
4. Prompt: "Read these search results and identify which companies just raised funding, hired a new exec, or had an outage"
5. Get structured output

---

## Research Workflow

### Step 1: Define Situational Trigger
From `analysis/situational_changes/hypotheses.md`:
- Post-funding
- New executive
- Outage
- etc.

### Step 2: Find Public Signals
Use appropriate tool:
- Funding → Crunchbase or Google News
- Executive hire → LinkedIn Sales Navigator
- Outage → Twitter/X search
- Job postings → LinkedIn

### Step 3: Save Research Snapshot
Create `research/snapshots/YYYY-MM-DD/[trigger_name]/`
- `serp_results.jsonl` - Raw search results
- `companies_found.csv` - Structured list of companies
- `synthesized_findings.md` - Your analysis

### Step 4: Pull Into Campaign
Use `pipelines/campaign_pull.py` to create `campaigns/*/pulled_customers.csv`

---

## Cost Tracking

**Monthly Research Budget**: $X

**Current Spend**:
- Serp.dev: $X
- LinkedIn Sales Navigator: $X
- Crunchbase: $X
- Total: $X

**Optimization**:
- Use free tools where possible (manual LinkedIn search vs. Sales Navigator)
- Batch API calls to save cost
- Cache results to avoid re-searching

---

**Last Updated**: _[YYYY-MM-DD]_
**Updated By**: _[Name]_
