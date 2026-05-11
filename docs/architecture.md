# Architecture

```
┌─────────────────────────────────────────────────────┐
│                    AI Agent                          │
│  (Claude Desktop · Cursor · VS Code · Custom)       │
└──────────────┬──────────────────────────────────────┘
               │ MCP Protocol (JSON-RPC over stdio)
               ▼
┌─────────────────────────────────────────────────────┐
│              Rental Agent MCP Server                 │
│                                                      │
│  ┌──────────┬──────────┬──────────┬──────────┐      │
│  │  Search  │Neighborhd │ Afford-  │ Compare  │      │
│  │  Listings│  Report   │  ability │          │      │
│  ├──────────┼──────────┼──────────┼──────────┤      │
│  │Roommate  │  Lease   │ Commute  │  Market  │      │
│  │ Calc     │ Analyzer │ Analysis │  Trends  │      │
│  └──────────┴──────────┴──────────┴──────────┘      │
│                                                      │
│  ┌──────────────────────────────────────────┐        │
│  │          Data Source Layer                │        │
│  │  ┌─────────┐ ┌─────────┐ ┌───────────┐   │        │
│  │  │OpenStreet│ │Nominatim│ │DuckDuckGo │   │        │
│  │  │   Map    │ │Geocoding│ │Web Search │   │        │
│  │  └─────────┘ └─────────┘ └───────────┘   │        │
│  │  ┌──────────────────────────────────┐    │        │
│  │  │     Built-in Calculations        │    │        │
│  │  │  (affordability, splits, scores) │    │        │
│  │  └──────────────────────────────────┘    │        │
│  └──────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## Design Principles

1. **Zero API keys** — Everything works out of the box. No signup, no billing, no rate limit anxiety.
2. **Stateless** — No database. No user accounts. No state to manage.
3. **Async** — httpx for concurrent requests, anyio for the MCP event loop.
4. **Composable** — Each tool does one thing well. Chain them for complex workflows.
5. **Portable** — Pure Python. Runs on any platform Python 3.10+ supports.

## Data Flow

1. AI agent sends tool request via MCP stdio protocol
2. Server routes to appropriate tool handler
3. Handler fetches external data (OSM, DuckDuckGo) or runs calculations
4. Results formatted as structured JSON
5. Response sent back to AI agent via stdio
