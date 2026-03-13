# AI-Assisted Development Workflow Tutorial

Learn a professional development workflow by building and deploying a real project: an e-commerce sales dashboard.

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌────────┐
│   PRD   │ -> │ spec-kit │ -> │  Jira   │ -> │  Code  │
│(written)│    │(Claude)  │    │(tracking)│    │(Claude)│
└─────────┘    └──────────┘    └─────────┘    └────────┘
                                                  │
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌────────┐
│  Live!  │ <- │  Deploy  │ <- │  Push   │ <- │ Commit │
│(public) │    │(Streamlit)│   │(GitHub) │    │(Git)   │
└─────────┘    └──────────┘    └─────────┘    └────────┘
```

See the finished product: https://sales-dashboard-greg-lontok.streamlit.app/

## Why this matters

Building with technology in 2026 looks different than it did two years ago. AI assistants have moved from experimental to essential, and companies are looking for people who can work with them effectively.

This isn't about becoming a software engineer. It's about being able to build solutions with technology and data -- dashboards, automated workflows, prototypes -- regardless of your specific role.

| Traditional approach | AI-assisted approach |
|---------------------|---------------------|
| Search Google, copy from Stack Overflow | Ask Claude Code to explain and implement |
| Hours debugging with print statements | AI analyzes errors and suggests fixes |
| Write boilerplate code manually | AI generates scaffolding; you focus on business logic |
| Learn frameworks by reading documentation | AI teaches you as you build |
| Work alone, limited by your own knowledge | AI as a second perspective when you get stuck |

## What you'll build

A Streamlit dashboard with KPI scorecards, a sales trend chart, and breakdowns by category and region. The dashboard itself is straightforward -- the point is the workflow you use to build it: writing a spec, tracking work in Jira, building with an AI assistant, committing with Git, and deploying so anyone can access it.

## How it works

You'll set up the same tools that development teams use, then build a dashboard from a product requirements document using AI-assisted development.

| Tool | What it does |
|------|-------------|
| GitHub | Hosts your code and tracks versions |
| Jira | Tracks tasks and requirements |
| Cursor | Code editor (VS Code-based, with AI features) |
| Claude Code | AI assistant that runs in your terminal |
| [spec-kit](https://github.com/github/spec-kit) | Turns requirements into a structured plan |
| Python + Streamlit | What you build the dashboard with |

## Getting started

### Version 2 (current)

Async pre-work + a 3-hour live workshop.

1. Start with [Pre-work: Setup](v2/pre-work-setup.md) -- accounts, tools, repo setup (60-90 min on your own)
2. Then [Workshop: Build & Deploy](v2/workshop-build-deploy.md) -- plan, build, and deploy the dashboard (~3 hours, live)

### Version 1 (original)

The original multi-document tutorial, designed for two 100-minute sessions.

| Order | Document | Description |
|:-----:|----------|-------------|
| 1 | [Overview](v1/00-overview.md) | What you'll build |
| 2 | [Session 1: Setup](v1/01-session-1-setup.md) | Accounts and tools |
| -- | [Terminal Basics](v1/02-terminal-basics.md) | Reference if you're new to the command line |
| -- | [Git Concepts](v1/03-git-concepts.md) | Reference if you're new to version control |
| 3 | [Session 2: Workflow](v1/04-session-2-workflow.md) | The full development workflow |

Reference materials: [Troubleshooting](v1/05-troubleshooting.md) · [Capstone Setup](v1/06-capstone-project-dev-environment.md) · [FAQ](v1/07-faq.md) · [Glossary](v1/08-glossary.md)

## Project materials

| Resource | Description |
|----------|-------------|
| [E-Commerce PRD](prd/ecommerce-analytics.md) | The product requirements document you'll build from |
| [Sales Data](data/sales-data.csv) | Sample dataset for the dashboard |

## Prerequisites

- Basic Python knowledge (pandas, simple scripts)
- A computer running macOS or Windows
- No prior experience with Git, Jira, or AI coding tools

## Getting help

Try to solve it yourself first. Google the error message, or if you have Claude Code installed, ask it. If you're still stuck, post in the Teams General channel.

## ShopSmart Sales Dashboard — Developer Reference

### Local setup

```bash
# 1. Install dependencies
uv sync

# 2. Run the dashboard (CSV mode — default)
uv run streamlit run app.py
```

Open http://localhost:8501 in your browser.

### Run tests

```bash
uv run pytest tests/ -v
```

All 25 tests should pass across `test_data`, `test_charts`, `test_integration`, and `test_smoke`.

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_DATABASE` | `false` | Set to `true` to load from an external database instead of CSV |
| `DB_CONNECTION_URL` | — | SQLAlchemy connection string (required when `USE_DATABASE=true`) |

```bash
# Example: run with a PostgreSQL database
export USE_DATABASE=true
export DB_CONNECTION_URL="postgresql://user:password@host:5432/dbname"
uv run streamlit run app.py
```

### Deploy to Streamlit Community Cloud

1. Push your branch to GitHub (repo must be public)
2. Go to https://share.streamlit.io → **New app**
3. Select your repo, branch, and set **Main file path** to `app.py`
4. For database mode, add secrets under **Advanced settings → Secrets** (TOML format):
   ```toml
   USE_DATABASE = "true"
   DB_CONNECTION_URL = "postgresql://..."
   ```
5. Click **Deploy**

## License

This tutorial is provided for educational purposes.
