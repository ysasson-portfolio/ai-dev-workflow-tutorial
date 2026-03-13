# Quickstart: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-12

---

## Prerequisites

```bash
git --version       # 2.x+
python --version    # 3.11+
uv --version        # any recent version
```

## 1. Clone and set up

```bash
git clone <your-fork-url>
cd <repo-name>
git checkout 001-sales-dashboard
```

## 2. Install dependencies

```bash
uv add streamlit plotly pandas sqlalchemy pytest
```

## 3. Run the dashboard locally (CSV mode)

```bash
uv run streamlit run app.py
```

Open http://localhost:8501 in your browser. The dashboard loads data from
`data/sales-data.csv` by default.

## 4. Run the dashboard with an external database (optional)

```bash
export USE_DATABASE=true
export DB_CONNECTION_URL="postgresql://user:password@host:5432/dbname"
uv run streamlit run app.py
```

When `USE_DATABASE=true`, the dashboard connects to the database instead of reading
the CSV. The database table must have the same schema as `data/sales-data.csv`.

## 5. Run tests

```bash
uv run pytest tests/ -v
```

Expected output: all tests pass. Run this before every commit that touches `data.py`
or `charts.py`.

### Run a specific test file

```bash
uv run pytest tests/test_data.py -v          # data pipeline unit tests
uv run pytest tests/test_charts.py -v        # chart builder unit tests
uv run pytest tests/test_integration.py -v   # full pipeline with real CSV
uv run pytest tests/test_smoke.py -v         # app import smoke tests
```

## 6. TDD workflow (required for data.py and charts.py)

For each new function:

```bash
# Step 1: Write the test — confirm it FAILS
uv run pytest tests/test_data.py::test_your_function -v
# Expected: FAILED

# Step 2: Write minimum implementation — confirm it PASSES
uv run pytest tests/test_data.py::test_your_function -v
# Expected: PASSED

# Step 3: Refactor — confirm still PASSES
uv run pytest tests/test_data.py::test_your_function -v
# Expected: PASSED
```

## 7. Deploy to Streamlit Community Cloud

1. Push your branch to GitHub (repo must be public)
2. Go to https://share.streamlit.io → New app
3. Select repo, branch `main` (or your branch), file `app.py`
4. If using a database: add `USE_DATABASE` and `DB_CONNECTION_URL` under
   **Advanced settings → Secrets** (TOML format):
   ```toml
   USE_DATABASE = "true"
   DB_CONNECTION_URL = "postgresql://..."
   ```
5. Click **Deploy**

## Validation checklist

After running locally, verify:

- [ ] Four KPI cards visible (Total Sales, Total Orders, AOV, Top Category)
- [ ] Total Sales ≈ $650,000–$700,000
- [ ] Total Orders = 482
- [ ] Trend line chart renders with Monthly granularity by default
- [ ] Daily/Monthly toggle re-renders the chart correctly
- [ ] Both bar charts (Category, Region) are sorted descending
- [ ] Sidebar filters (date range, category, region) update all views
- [ ] All `pytest` tests pass
- [ ] No errors or warnings in the Streamlit console
