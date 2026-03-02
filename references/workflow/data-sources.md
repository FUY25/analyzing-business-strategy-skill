# Data Sources Reference

## MCP Servers

### Octagon MCP (Company & Financial Data)
- **Setup:** `npx -y octagon-mcp@latest` with `OCTAGON_API_KEY`
- **Coverage:** SEC filings (10-K, 10-Q, 8-K, 20-F, S-1) for 8000+ companies, earnings call transcripts (10yr history), financial metrics/ratios, stock data (10,000+ tickers), private company research (3M+ companies), funding rounds/VC (500k+ deals), M&A/IPO transactions (2M+ deals), institutional holdings/13F filings
- **Free tier:** Yes, sign up at app.octagonai.co
- **Best for:** Company-level analysis, due diligence, competitive benchmarking

### Yahoo Finance MCP (Stock & Market Data)
- **Setup:** `uvx mcp-yahoo-finance`
- **Coverage:** Stock pricing, company info, options chains, historical prices
- **Cost:** Free, no API key
- **Best for:** Quick stock data, company snapshots

### FRED MCP (US Macro Data)
- **Setup:** `uv run` with `FRED_API_KEY` (Free API key at fred.stlouisfed.org/docs/api/api_key.html)
- **Coverage:** 800K+ economic time series — GDP, CPI, unemployment, interest rates, money supply, trade balance, consumer confidence, housing
- **Best for:** US macroeconomic context, interest rate environment, inflation trends

### AkShare MCP (China Macro & Financial Data)
- **Setup:** `uv run akshare-mcp` (ttjslbz001/akshare_mcp_server)
- **Coverage:** China GDP, CPI, PMI, PPI, money supply, trade data, industrial output, retail sales, property prices, plus A-share stocks/funds/futures/forex
- **Cost:** Free, no API key
- **Best for:** China market entry, APAC strategy, China macro context

### Brave Search MCP (Web Research)
- **Setup:** Part of official MCP servers
- **Coverage:** General web search
- **Best for:** Industry reports, competitive intelligence, qualitative research

---

## Free APIs (No MCP — Use via Sub-Agent Scripts)

### Europe
| API | Coverage | Access |
|-----|----------|--------|
| Eurostat REST API | EU GDP, HICP inflation, unemployment, trade, industrial production, government debt | Free, no key. `ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/` |
| ECB Statistical Data Warehouse | ECB rates, exchange rates, M1/M2/M3, balance of payments, bank lending | Free, no key. `data.ecb.europa.eu/help/api/overview` |

**Python libraries:** `eurostat`, `sdmx1`, `pandasdmx`

### Global / Multi-Country
| API | Coverage | Access |
|-----|----------|--------|
| World Bank API | 200+ countries, 1600+ indicators (GDP, population, poverty, trade, health) | Free, no key. `api.worldbank.org/v2/` |
| IMF Data API | WEO, IFS, Balance of Payments, 190+ countries | Free, no key. `dataservices.imf.org/REST/SDMX_JSON.svc/` |
| OECD Data API | 38 OECD countries — GDP, CPI, unemployment, trade, productivity | Free, no key. `sdmx.oecd.org/public/rest/` |
| DBnomics | Aggregates 80+ providers (ECB, Eurostat, IMF, OECD, Fed) | Free, no key. `api.db.nomics.world/v22/` |

**Python libraries:** `wbgapi`, `sdmx1`, `imfp`, `fredapi`, `dbnomics`

### China (Alternative to AkShare MCP)
| API | Coverage | Access |
|-----|----------|--------|
| Tushare Pro | A-share stocks, macro indicators (GDP, CPI, M2, Shibor) | Free tier + paid. `tushare.pro` |
| NBS (National Bureau of Statistics) | Official China GDP, CPI, industrial output, retail sales | Free, no key. `data.stats.gov.cn` |

---

## Data Sourcing Decision Tree

```
User has internal data?
├── Yes → Incorporate it first, supplement with public data
└── No → Ask if they know where to find relevant data
         ├── Yes → Help them access it
         └── No → Use this priority:
              1. MCP tools (fastest, structured)
              2. Free public APIs via scripts
              3. Web search for reports/qualitative data
              4. Consumer feedback sources (see below)
              5. Note gaps transparently
```

---

## Consumer Feedback & Demand Signal Sources

Use these to gather real consumer sentiment, reviews, and demand signals. Layer multiple sources: Reddit for qualitative depth, Google Trends for quantitative demand, industry-specific sites for structured comparisons.

### Tier 1: High-Access, Rich Qualitative Data

| Source | URL | What it provides | Agent access |
|--------|-----|-----------------|--------------|
| Reddit | reddit.com | Unfiltered consumer opinions, complaints, comparisons. Niche subreddits for any industry. | Append `.json` to any URL (e.g., `old.reddit.com/r/HomeImprovement/top.json?t=month`). No auth. |
| Google Trends | trends.google.com | Search interest over time, regional demand, related queries, rising topics. | Use `pytrends` Python library (no auth). Or fetch web pages. |
| Trustpilot | trustpilot.com | Star ratings + written reviews for businesses (e-commerce, services, fintech). | Public pages, easy to fetch. |
| Hacker News | news.ycombinator.com | Tech-savvy consumer/developer opinions on products, startups, tools. | Free REST API (no auth): `hacker-news.firebaseio.com/v0/` |
| Product Hunt | producthunt.com | Early adopter reactions, upvotes, feature requests for new products. | Public pages fetchable. GraphQL API available. |

### Tier 2: Industry-Specific Review Sites

| Source | URL | Best for | Agent access |
|--------|-----|----------|--------------|
| G2 | g2.com | B2B software — structured pros/cons, feature ratings, comparison grids | Public pages fetchable |
| Capterra | capterra.com | B2B software — reviews, pricing data, feature comparisons | Public pages fetchable |
| Houzz | houzz.com | Home improvement, interior design, construction | Public pages fetchable |
| ConsumerAffairs | consumeraffairs.com | Insurance, home services, finance, consumer products | Public pages fetchable |
| TripAdvisor | tripadvisor.com | Hospitality, travel, restaurants | Public pages fetchable |
| Edmunds / Cars.com | edmunds.com, cars.com | Automotive — expert + consumer reviews | Public pages fetchable |
| App Store / Google Play | apps.apple.com, play.google.com | Mobile app ratings and reviews | Google Play fetchable; Apple JS-heavy |

### Tier 3: Review Analysis & Authenticity Tools

| Source | URL | What it provides | Agent access |
|--------|-----|-----------------|--------------|
| ReviewMeta | reviewmeta.com | Adjusted Amazon ratings filtering fake reviews | Append ASIN to URL for analysis |
| Fakespot | fakespot.com | Review authenticity grading for Amazon, Walmart, eBay | Public analysis pages |

### Tier 4: Macro Consumer Research

| Source | URL | What it provides | Agent access |
|--------|-----|-----------------|--------------|
| Pew Research | pewresearch.org | Large-scale surveys on tech adoption, consumer behavior, demographics | Articles and data tables fetchable |
| Statista | statista.com | Aggregated stats, survey results, market forecasts | Preview data public; full reports paid |
| Census Bureau | census.gov | Consumer expenditure, demographics | Free public APIs |
| BLS | bls.gov | Consumer price index, spending patterns | Free public APIs |

### How to Use in Strategy Engagements

**For any consumer-facing analysis, agents should check at minimum:**
1. **Reddit** — search relevant subre the product/industry. Look for complaint patterns, unmet needs, brand sentiment, purchase decision factors.
2. **Google Trends** — compare search interest for the client's category vs. competitors. Check geographic and seasonal patterns.
3. **Industry-specific review site** — pick the one most relevant to the domain (G2 for SaaS, Houzz for home improvement, etc.).

**Reddit search patterns for agents:**
```bash
# Top posts in a subreddit (JSON, no auth)
curl -s "https://old.reddit.com/r/HomeImprovement/search.json?q=paint+brand&sort=relevance&t=year&limit=25"

# Top comments on a specific post
curl -s "https://old.reddit.com/r/HomeImprovement/comments/<post_id>.json"

# Search across all of Reddit
curl -s "https://old.reddit.com/search.json?q=best+eco+paint&sort=relevance&t=year&limit=25"
```

**Google Trends via Python:**
```python
from pytrends.request import TrendReq
pytrends = TrendReq()
pytrends.build_payload(["eco paint", "zero VOC paint", "Clare paint"], timeframe="today 12-m")
interest = pytrends.interest_over_time()
```
