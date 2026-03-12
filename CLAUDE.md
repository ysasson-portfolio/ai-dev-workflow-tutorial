# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A tutorial repository teaching AI-assisted development workflow. It contains documentation (Markdown) and sample data — no buildable application code lives here. Students fork this repo and build a Streamlit dashboard as part of the workshop.

The workflow the tutorial teaches:
```
PRD -> spec-kit -> Jira -> Code -> Commit -> Push -> Deploy (Streamlit Cloud)
```

## Repository structure

```
prd/ecommerce-analytics.md   # The PRD students build from
data/sales-data.csv          # Sample sales dataset (1,000 rows, 8 columns)
v1/                          # Original tutorial (two 100-min sessions)
v2/                          # Current tutorial (pre-work + 3-hr workshop)
  pre-work-setup.md          # Accounts, tools, repo setup (~60-90 min async)
  workshop-build-deploy.md   # Spec-kit, Jira, build, deploy (~3 hrs live)
  README.md                  # v2 overview
```

## The dashboard students build

A Streamlit app (`app.py`) with:
- KPI scorecards: Total Sales (~$650-700K), Total Orders (482)
- Line chart: sales trend over time
- Two bar charts: sales by category, sales by region
- Stack: Python 3.11+, Streamlit, Plotly, Pandas
- Data source: `data/sales-data.csv`

## Tools referenced in the tutorial

| Tool | Purpose |
|------|---------|
| `uv` | Python package manager (preferred over pip) |
| `spec-kit` | Turns a PRD into constitution → specification → plan → tasks |
| Claude Code | AI assistant in the terminal |
| Atlassian Rovo MCP | Connects Claude Code to Jira |
| Streamlit Community Cloud | Free deployment target |

## Commit convention

Commit messages should include the Jira issue key, e.g.:
```
ECOM-1: Set up project environment and data loading
```

## When editing tutorial content

- v2 is the current version; v1 is the original (kept for reference)
- Both versions teach the same workflow but are structured differently
- The finished dashboard reference: https://sales-dashboard-greg-lontok.streamlit.app/
- Verify tool/UI instructions against current versions — onboarding flows change frequently (Streamlit, GitHub, Atlassian, Claude)

## Student environment setup (from pre-work)

```bash
# Verify prerequisites
git --version          # 2.x+
python --version       # 3.11+
uv --version
spec-kit --version
claude --version

# Install dashboard dependencies (students run this)
uv add streamlit plotly pandas

# Run the dashboard locally
uv run streamlit run app.py
```

## Active Technologies
- Python 3.11+ + Streamlit, Pandas, Plotly, SQLAlchemy (optional, DB path only), pytest (001-sales-dashboard)
- `data/sales-data.csv` (default); external relational DB via `USE_DATABASE=true` + `DB_CONNECTION_URL` env vars (001-sales-dashboard)

## Recent Changes
- 001-sales-dashboard: Added Python 3.11+ + Streamlit, Pandas, Plotly, SQLAlchemy (optional, DB path only), pytest
