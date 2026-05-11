<p align="center">
  <br>
  <img src="https://img.shields.io/badge/Rental%20Agent-MCP-8A2BE2?style=for-the-badge&logo=python&logoColor=white" alt="Rental Agent MCP">
</p>

<h1 align="center">🏠 Rental Agent</h1>
<h3 align="center">The AI-native rental intelligence platform. 8 tools. Zero API keys. One command.</h3>

<br>

<p align="center">
  <a href="https://github.com/Rumblingb/rental-agent-mcp/stargazers">
    <img src="https://img.shields.io/github/stars/Rumblingb/rental-agent-mcp?style=flat-square&logo=github&color=gold" alt="GitHub Stars">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/MCP-1.0%2B-purple?style=flat-square" alt="MCP 1.0+">
  </a>
  <a href="#contributing">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status: Active">
  </a>
  <a href="https://smithery.ai/server/@Rumblingb/rental-agent-mcp">
    <img src="https://img.shields.io/badge/deploy-smithery-FF6B6B?style=flat-square&logo=vercel&logoColor=white" alt="Deploy on Smithery">
  </a>
</p>

<br>

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🎯 Use Cases](#-use-cases)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🔧 Tool Reference](#-tool-reference)
- [🗺️ Data Sources](#️-data-sources)
- [💰 Pricing](#-pricing)
- [🌐 API (Non-MCP)](#-api-non-mcp)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Quick Start

**Get a fully functional rental AI agent in 30 seconds.**

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
python3 server.py

# 3. Add to Claude Desktop (see configuration below)
# Done. Your AI can now search listings, analyze neighborhoods,
# check affordability, compare options, review leases, and more.
```

**That's it.** No API keys. No database setup. No Docker required (though we support it). Just Python and an internet connection.

> **Prerequisites:** Python 3.10+, `pip`, and an internet connection for location & listing data.

---

## ✨ Features

Rental Agent packs **8 purpose-built tools** covering the entire rental workflow — from finding a place to signing the lease.

| # | Tool | Description |
|---|------|-------------|
| 🔍 | `rental_search_listings` | Search for current rental listings in any city with price, bedroom, and result filters |
| 🏘️ | `rental_neighborhood_report` | Get a comprehensive neighborhood report: amenities, transit stops, parks, schools, and hospitals within 1km |
| 💰 | `rental_affordability` | Calculate how much rent you can afford using the 30% rule or 50/30/20 budget framework |
| ⚖️ | `rental_compare` | Compare multiple listings side-by-side with auto-generated scores (0–100) |
| 👥 | `rental_roommate_calculator` | Split rent fairly — equal split, by room size, by income, or a combined method |
| 📜 | `rental_lease_analyzer` | Analyze lease text for key terms, hidden fees, and red flags (late fees, pet policies, eviction clauses) |
| 🚗 | `rental_commute_analysis` | Estimate drive/transit time and monthly commuting costs between two locations |
| 📈 | `rental_market_trends` | Get rental market context, estimated affordability, and city-level income benchmarks |

**Why these tools?** Each one solves a concrete problem renters face. Combined, they form an end-to-end rental assistant that would normally require 5+ different websites and a spreadsheet.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        YOUR AI AGENT                                 │
│            (Claude Desktop, Cursor, VS Code, Copilot, etc.)          │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     Model Context Protocol (MCP)                     │
│                           StdIO Transport                            │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         RENTAL AGENT MCP                             │
│                                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Search      │  │ Neighborhood │  │ Afford-     │  │ Compare   │ │
│  │ Listings    │  │ Report       │  │ ability     │  │ Listings  │ │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                 │               │       │
│  ┌──────┴──────┐  ┌──────┴───────┐  ┌──────┴──────┐  ┌─────┴─────┐ │
│  │ Roommate    │  │ Lease        │  │ Commute     │  │ Market    │ │
│  │ Calculator  │  │ Analyzer     │  │ Analysis    │  │ Trends    │ │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                 │               │       │
└─────────┼────────────────┼─────────────────┼───────────────┼───────┘
          │                │                 │               │
          ▼                ▼                 ▼               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                                    │
│                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐   │
│  │  OpenStreetMap  │  │   Nominatim    │  │    DuckDuckGo        │   │
│  │  (Overpass API)  │  │  (Geocoding)   │  │   (Web Search)       │   │
│  │  Amenities,     │  │  Lat/Lon from  │  │  Rental listings,    │   │
│  │  transit, parks │  │  place names   │  │  market data         │   │
│  └────────────────┘  └────────────────┘  └──────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Built-in Calculations Engine                     │   │
│  │  Affordability math │ Rent splitting │ Commute estimation     │   │
│  │  Comparison scoring │ Lease text analysis │ Market insights   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

**Zero external dependencies for data.** All sources are free, open, and require no API keys. The calculation engine is built into the server itself.

---

## 🎯 Use Cases

### 🏠 Apartment Hunting
Search listings, compare options with scores, and check neighborhood walkability — all in one conversation.

> *"Find me 2-bedroom apartments in Austin TX under $2,000, compare the top 3, and tell me about the neighborhoods."*

### 🗺️ Relocation Planning
Moving to a new city? Get neighborhood reports, commute estimates, and market trends before you visit.

> *"I'm moving to Seattle for a job in South Lake Union. What neighborhoods are within a 30-minute commute and what's the average 1-bedroom rent?"*

### 💰 Budget Planning
Know exactly what you can afford before you start looking. No surprises.

> *"I make $72,000 a year with $400 in monthly student loans. What rent can I afford using the 50/30/20 rule?"*

### 👥 Roommate Coordination
Fair rent splitting prevents arguments. Choose equal, by-room-size, by-income, or a hybrid.

> *"Split $3,200 rent between Alice (150 sqft, $50k income), Bob (120 sqft, $60k), and Carol (130 sqft, $45k) using the combined method."*

### 📜 Lease Review
Catch red flags, hidden fees, and unfavorable terms before you sign.

> *"Here's my lease agreement. Can you analyze it for late fees, pet policy, subleasing restrictions, and maintenance obligations?"*

### 🚗 Commute Optimization
Compare neighborhoods by commute time and cost. The 45-minute threshold can save you thousands.

> *"Compare commute times from Downtown Austin vs Mueller vs East Austin to my office at 78701."*

---

## 📦 Installation

### pip (Recommended)

```bash
git clone https://github.com/Rumblingb/rental-agent-mcp.git
cd rental-agent-mcp
pip install -r requirements.txt
python3 server.py
```

### uv (Fastest Python package manager)

```bash
git clone https://github.com/Rumblingb/rental-agent-mcp.git
cd rental-agent-mcp
uv pip install -r requirements.txt
python3 server.py
```

### Docker

```bash
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  python:3.11-slim \
  bash -c "pip install -r requirements.txt && python3 server.py"
```

### Manual (From Source)

```bash
git clone https://github.com/Rumblingb/rental-agent-mcp.git
cd rental-agent-mcp
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcp httpx
python3 server.py
```

### Smithery (Cloud Deployment)

[![Deploy on Smithery](https://img.shields.io/badge/deploy-smithery-FF6B6B?style=for-the-badge&logo=vercel&logoColor=white)](https://smithery.ai/server/@Rumblingb/rental-agent-mcp)

One-click deployment to Smithery's cloud infrastructure. No local setup required.

---

## ⚙️ Configuration

### Environment Variables

**None required.** Rental Agent works out of the box with zero configuration.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| — | ❌ | — | No env vars needed. Truly plug-and-play. |

### Claude Desktop

1. Open **Claude Desktop Settings** → **Developer** → **Edit Config**
2. Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rental-agent": {
      "command": "python3",
      "args": ["/path/to/rental-agent-mcp/server.py"]
    }
  }
}
```

### VS Code (Cline / Continue)

For **Continue** extension in VS Code, add to your `~/.continue/config.json`:

```json
{
  "experimental": {
    "mcpServers": {
      "rental-agent": {
        "command": "python3",
        "args": ["/path/to/rental-agent-mcp/server.py"]
      }
    }
  }
}
```

For **Cline** extension, configure in Cline settings → MCP Servers:

```json
{
  "mcpServers": {
    "rental-agent": {
      "command": "python3",
      "args": ["/path/to/rental-agent-mcp/server.py"]
    }
  }
}
```

### Cursor

1. Open **Cursor Settings** → **Features** → **MCP Servers**
2. Click **Add New MCP Server**
3. Set **Name**: `rental-agent`
4. Set **Type**: `command`
5. Set **Command**: `python3 /path/to/rental-agent-mcp/server.py`
6. Click **Save**

---

## 🔧 Tool Reference

### 🔍 `rental_search_listings`

Search for current rental listings in any city using web search aggregation.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `location` | string | ✅ | — | City, state, or neighborhood (e.g. `"Austin TX"`, `"Brooklyn NY"`) |
| `min_price` | integer | ❌ | — | Minimum monthly rent filter |
| `max_price` | integer | ❌ | — | Maximum monthly rent filter |
| `bedrooms` | integer | ❌ | — | Number of bedrooms filter |
| `max_results` | integer | ❌ | `5` | Maximum number of results to return |

**Example:**

```json
{
  "location": "Austin TX",
  "max_price": 2000,
  "bedrooms": 2,
  "max_results": 3
}
```

---

### 🏘️ `rental_neighborhood_report`

Get a comprehensive neighborhood report powered by OpenStreetMap data.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `location` | string | ✅ | — | Neighborhood or city (e.g. `"Williamsburg Brooklyn"`, `"Downtown Austin"`) |

**Returns:** Restaurants, cafes, bars, supermarkets, gyms, parks, pharmacies, libraries counts within ~1km, plus transit stops, schools, and hospitals.

**Example:**

```json
{
  "location": "Williamsburg Brooklyn"
}
```

**Sample output:**

```json
{
  "neighborhood": "Williamsburg, Brooklyn, Kings County, New York, 11211, USA",
  "walkability": {
    "restaurants": 34,
    "cafes": 12,
    "bars": 18,
    "supermarkets": 4,
    "gyms": 3,
    "pharmacies": 2
  },
  "transit": { "transit_stops_nearby": 9 },
  "schools_nearby": 5,
  "walkability_note": "Higher amenity counts = more walkable. 5+ restaurants + cafes in 1km = very walkable."
}
```

---

### 💰 `rental_affordability`

Calculate how much rent you can afford based on your income and expenses.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `annual_income` | number | ✅ | — | Annual pre-tax income in USD |
| `monthly_debt` | number | ❌ | `0` | Monthly debt payments (loans, credit cards) |
| `rule` | string | ❌ | `"30_percent"` | Budget rule: `"30_percent"` or `"50_30_20"` |

**Budget Rules:**

- **30% Rule:** Max rent = 30% of monthly gross income (landlord standard)
- **50/30/20 Rule:** 50% needs (rent within), 30% wants, 20% savings

**Example:**

```json
{
  "annual_income": 75000,
  "monthly_debt": 300,
  "rule": "30_percent"
}
```

---

### ⚖️ `rental_compare`

Compare multiple rental options side-by-side with auto-generated scores (0–100).

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `listings_json` | string | ✅ | — | JSON array of listings with name, price, bedrooms, sqft, neighborhood |

**Listing format:**

```json
{
  "listings_json": "[{\"name\":\"Modern Downtown Studio\",\"price\":1800,\"bedrooms\":1,\"sqft\":650,\"neighborhood\":\"Downtown\"},{\"name\":\"East Side 2BR\",\"price\":2200,\"bedrooms\":2,\"sqft\":950,\"neighborhood\":\"East Austin\"},{\"name\":\"North Campus Studio\",\"price\":1200,\"bedrooms\":1,\"sqft\":500,\"neighborhood\":\"North Campus\"}]"
}
```

**Scoring logic:** Lower price = better score, more bedrooms = bonus, higher sqft = bonus, low $/sqft = bonus. Scores range 0–100.

---

### 👥 `rental_roommate_calculator`

Split rent fairly among roommates using one of four methods.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `total_rent` | number | ✅ | — | Total monthly rent |
| `roommates_json` | string | ✅ | — | JSON array of roommates with name, room_size_sqft, income |
| `method` | string | ❌ | `"by_room"` | Method: `"equal"`, `"by_room"`, `"by_income"`, or `"combined"` |

**Methods:**

| Method | Description |
|--------|-------------|
| `equal` | Everyone pays the same amount |
| `by_room` | Split proportional to each person's room square footage |
| `by_income` | Split proportional to each person's income (progressive) |
| `combined` | 50% by room size + 50% by income (fairest for most situations) |

**Example:**

```json
{
  "total_rent": 3200,
  "roommates_json": "[{\"name\":\"Alice\",\"room_size_sqft\":150,\"income\":50000},{\"name\":\"Bob\",\"room_size_sqft\":120,\"income\":60000},{\"name\":\"Carol\",\"room_size_sqft\":130,\"income\":45000}]",
  "method": "combined"
}
```

---

### 📜 `rental_lease_analyzer`

Analyze lease text for key terms, hidden fees, and red flags.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lease_text` | string | ✅ | — | Full text of the lease agreement |

**What it detects:**

| Category | Checks |
|----------|--------|
| **Terms** | Monthly rent amount, lease duration, security deposit |
| **Fees** | Late payment fees, pet fees/deposits |
| **Red Flags** | No subleasing, guest restrictions, eviction clauses, short inspection notice |
| **Key Clauses** | Utilities, parking, maintenance, renewal, termination |

> ⚠️ **Disclaimer:** This tool provides informational analysis only and does not constitute legal advice. Always consult a lawyer for important lease decisions.

---

### 🚗 `rental_commute_analysis`

Estimate commute time and monthly cost between two locations.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `from_location` | string | ✅ | — | Your rental location or neighborhood |
| `to_location` | string | ✅ | — | Your workplace or destination |
| `commute_days_per_month` | integer | ❌ | `20` | Days you commute per month |

**What it calculates:**

- Straight-line distance (km and miles)
- Estimated drive time (avg 50 km/h city speed)
- Estimated transit time (avg 30 km/h + 10 min walk/wait)
- Monthly driving cost (IRS rate: $0.60/mile)
- Monthly transit cost (~$0.15/km)

**Example:**

```json
{
  "from_location": "Mueller Austin",
  "to_location": "Downtown Austin",
  "commute_days_per_month": 22
}
```

---

### 📈 `rental_market_trends`

Get rental market context and price trends for any city.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `city` | string | ✅ | — | City name (e.g. `"Austin, TX"`, `"Seattle, WA"`) |

**Returns:** Web search results for average rental prices, plus estimated affordability based on median income benchmarks for major US cities (NYC, SF, LA, Chicago, Austin, Seattle, Boston, Denver, Miami, Portland, Nashville, Atlanta, Phoenix, Dallas, Houston).

**Example:**

```json
{
  "city": "Denver, CO"
}
```

---

## 🗺️ Data Sources

Rental Agent uses **three free, open data sources** — no API keys needed, ever.

### OpenStreetMap (Overpass API)
**What we use it for:** Neighborhood amenities, transit stops, parks, schools, hospitals.
**Why it's free:** OSM is the Wikipedia of maps — a global community of mappers contributing open geographic data.
**Reliability:** Used by Apple Maps, Amazon, Meta, and thousands of other organizations. Updated continuously.
**Rate limits:** Generous — suitable for hundreds of queries per day.
**No account needed:** Public API, anonymous access.

### Nominatim (OSM Geocoder)
**What we use it for:** Converting place names ("Williamsburg Brooklyn") to precise latitude/longitude coordinates.
**Why it's free:** Operated by the OSM Foundation as a public service.
**Reliability:** Powers geocoding for millions of applications worldwide.
**Usage policy:** 1 request per second recommended (we use async with automatic spacing).

### DuckDuckGo Instant Answers API
**What we use it for:** Searching for current rental listings and market trend data.
**Why it's free:** DuckDuckGo provides a public API for non-commercial use.
**Reliability:** Returns structured results from Wikipedia, Wikidata, and DuckDuckGo's index.
**No rate limiting:** Generous access with no API key required.

### Built-in Calculations Engine
All financial calculations (affordability, rent splitting, commute costs, comparison scoring, lease analysis) run **locally** on the server — no external API calls needed.

---

## 💰 Pricing

| Feature | Free | Pro |
|---------|:----:|:---:|
| **Price** | **$0** | **$19/mo** |
| **Daily queries** | 50/day | Unlimited |
| **All 8 tools** | ✅ | ✅ |
| **All data sources** | ✅ | ✅ |
| **Zero API keys** | ✅ | ✅ |
| **Neighborhood reports** | ✅ | ✅ |
| **Lease analysis** | ✅ | ✅ |
| **Commute analysis** | ✅ | ✅ |
| **Market trends** | ✅ | ✅ |
| **Roommate calculator** | ✅ | ✅ |
| **Priority support** | ❌ | ✅ |
| **Early access to new tools** | ❌ | ✅ |

**Get Pro:** [Subscribe Now](https://buy.stripe.com/dRm6oJ4Hd2Jugek0wz1oI0m)

The free tier handles 50 queries/day — enough for casual apartment hunting. The Pro tier removes all limits for power users, real estate professionals, and teams.

---

## 🌐 API (Non-MCP)

You can also use Rental Agent as a standalone REST API server. This is useful if you want to integrate rental intelligence into your own application without the MCP protocol.

### Quick Start (REST Mode)

```python
from server import rental_search_listings, rental_neighborhood_report
import asyncio

async def main():
    # Search listings
    listings = await rental_search_listings(
        location="Austin TX",
        max_price=2000,
        bedrooms=2
    )
    print(listings)

    # Get neighborhood report
    report = await rental_neighborhood_report(
        location="Downtown Austin"
    )
    print(report)

asyncio.run(main())
```

### Building a REST Wrapper

```python
from fastapi import FastAPI
from server import rental_search_listings, rental_neighborhood_report
import asyncio

app = FastAPI()

@app.get("/search")
async def search(location: str, max_price: int = None, bedrooms: int = None):
    result = await rental_search_listings(
        location=location,
        max_price=max_price,
        bedrooms=bedrooms
    )
    return result

@app.get("/neighborhood")
async def neighborhood(location: str):
    result = await rental_neighborhood_report(location=location)
    return result
```

All 8 tools are async Python functions that accept the same parameters and return JSON strings — ready to be wrapped in any web framework.

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to get started:

### Development Setup

```bash
git clone https://github.com/Rumblingb/rental-agent-mcp.git
cd rental-agent-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ways to Contribute

- **🐛 Report bugs** — Open an issue with a clear reproduction
- **💡 Suggest features** — New tools, data sources, or integrations
- **📝 Improve docs** — Better examples, clearer explanations
- **🔧 Submit PRs** — Code improvements, bug fixes, new tools

### Guidelines

1. Fork the repo and create a feature branch
2. Write clean, typed Python with docstrings
3. Test your changes locally with `python3 server.py`
4. Open a PR with a clear description of what you changed and why
5. Keep it simple — this project values clarity over cleverness

### Roadmap Ideas

- [ ] Zillow / Apartments.com direct API integration
- [ ] Crime data overlay via open crime databases
- [ ] School rating integration (GreatSchools API)
- [ ] Transit time calculation using open GTFS data
- [ ] Floor plan visualization analysis
- [ ] Rent history tracking and prediction
- [ ] Multi-language lease analysis

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.

```
MIT License

Copyright (c) 2025 Rumblingb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

<p align="center">
  <b>🏠 Rental Agent</b> — AI-native rental intelligence for the MCP ecosystem.
  <br>
  Built with ❤️ by <a href="https://github.com/Rumblingb">Rumblingb</a>
  <br>
  <br>
  <a href="https://github.com/Rumblingb/rental-agent-mcp">GitHub</a>
  ·
  <a href="https://buy.stripe.com/dRm6oJ4Hd2Jugek0wz1oI0m">Pricing</a>
  ·
  <a href="https://smithery.ai/server/@Rumblingb/rental-agent-mcp">Smithery</a>
  ·
  <a href="#-quick-start">Quick Start</a>
  ·
  <a href="#-contributing">Contributing</a>
  <br>
  <br>
  <sub>Zero API keys. Infinite possibilities.</sub>
</p>
