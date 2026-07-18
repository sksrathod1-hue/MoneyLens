# System Design Document - MoneyLens

## Architecture Overview
MoneyLens follows a decoupled client-server architecture:

```
┌──────────────────┐            HTTP / JSON            ┌──────────────────┐
│  Web Frontend    │ ◄───────────────────────────────► │   Flask Backend  │
│  (HTML/CSS/JS)   │                                   │     REST API     │
└──────────────────┘                                   └────────┬─────────┘
                                                                │
                                                                ▼
                                                       ┌──────────────────┐
                                                       │  SQLite Database │
                                                       └──────────────────┘
```

## Core Modules
1. **Frontend App Client**: Loads modules dynamically. Dispatches HTTP requests through a shared `MoneyLensAPI` wrapper.
2. **API Blueprint Server**: Flask routes parsing JSON requests, checking middleware guards, and returning serialized structures.
3. **Database Layer**: SQLite relational storage with models defined via SQLAlchemy ORM.
4. **Ingestion Engine**: Regex parser extracting transaction data from plain SMS structures.
5. **AI Services Node**: Analytical rules engine generating insights with Gemini API hook capability.
