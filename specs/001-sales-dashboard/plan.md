# Implementation Plan: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-sales-dashboard/spec.md`

## Summary

Build a Streamlit single-page dashboard that visualises ShopSmart sales data from a CSV
file (with optional external database support via feature flag). The dashboard displays
four KPI scorecards, a time-series trend chart with daily/monthly granularity toggle,
and two segment bar charts. All views respond to a shared filter state (date range,
category, region) stored in Streamlit session state. Logic is split across three modules
(`data.py`, `charts.py`, `app.py`) to enable TDD for all non-UI code.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit, Pandas, Plotly, SQLAlchemy (optional, DB path only), pytest
**Storage**: `data/sales-data.csv` (default); external relational DB via `USE_DATABASE=true` + `DB_CONNECTION_URL` env vars
**Testing**: pytest — unit tests for `data.py` and `charts.py`, integration test with real CSV, smoke tests for `app.py`
**Target Platform**: Streamlit Community Cloud (production), local `uv run streamlit run app.py` (development)
**Project Type**: Single-page web application (dashboard)
**Performance Goals**: Full page load ≤ 5 s; filter/granularity re-render ≤ 2 s
**Constraints**: Public repo required for free Streamlit Cloud tier; no auth in Phase 1; secrets via Streamlit Cloud Secrets UI
**Scale/Scope**: ~1,000 CSV rows; single-user sessions; one deployment target

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Data-Source Flexibility | ✅ PASS | CSV default; `USE_DATABASE` flag activates SQLAlchemy DB path |
| II. Streamlit-Native Visualization | ✅ PASS | `st.metric`, `st.line_chart`/`st.bar_chart` preferred; Plotly fallback documented at call site |
| III. Test-First Development | ✅ PASS | Full test suite: unit + integration + smoke; tests written before implementation |
| IV. Deploy to Streamlit Community Cloud | ✅ PASS | Single prod target; dependencies in `pyproject.toml`; secrets in Streamlit UI |
| V. Simplicity First (YAGNI) | ✅ PASS | Three modules justified by testability requirement (Principle III); no further abstractions |

**Post-Phase 1 re-check**: All gates still pass. Three-module split is the minimum needed
for TDD compliance; SQLAlchemy dependency is isolated behind a feature flag and adds no
complexity to the CSV path.

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── data-interface.md
│   └── charts-interface.md
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
app.py               # Streamlit entry point: page config, sidebar filters,
                     # session state init, layout, chart rendering calls
data.py              # load_data(), filter_data(), compute_kpis(),
                     # aggregate_by_time(), aggregate_by_column()
charts.py            # build_trend_chart(), build_bar_chart()
pyproject.toml       # uv-managed dependencies
data/
└── sales-data.csv   # Source data (1,000 rows)
tests/
├── test_data.py     # Unit tests for all data.py functions (TDD)
├── test_charts.py   # Unit tests for chart data-prep in charts.py (TDD)
├── test_integration.py  # Full pipeline: load → filter → aggregate → chart data
└── test_smoke.py    # Import app.py; verify no errors on module load
```

**Structure Decision**: Three-module structure selected. `data.py` and `charts.py` expose
pure functions that can be tested without a running Streamlit server. `app.py` is the
thin UI layer that wires session state to these functions. This satisfies Constitution
Principle III (TDD) while staying within Principle V (YAGNI) — no further split is needed.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| Two extra modules (`data.py`, `charts.py`) beyond single `app.py` | TDD (Principle III) requires pure functions testable without Streamlit | All logic in `app.py` cannot be unit-tested without a running Streamlit server |
| SQLAlchemy dependency | Constitution Principle I requires external DB support | No lighter-weight alternative supports the variety of target databases (Postgres, BigQuery, SQLite) |
