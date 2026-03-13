# Research: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-12
**Branch**: `001-sales-dashboard`

---

## 1. Charting Library Strategy

**Decision**: Streamlit-native primitives first (`st.metric`, `st.line_chart`,
`st.bar_chart`); Plotly (`st.plotly_chart`) as approved fallback.

**Rationale**: Constitution Principle II mandates this order. For this dashboard:
- KPI scorecards → `st.metric` (native, no Plotly needed)
- Trend line chart → `st.line_chart` sufficient for labeled time-series; Plotly fallback
  only if tooltip formatting or granularity toggle cannot be achieved natively
- Bar charts → `st.bar_chart` sufficient for sorted category/region bars; Plotly fallback
  if descending sort or tooltip customisation requires it

**Alternatives considered**:
- Altair: rejected — not in approved list per Principle II
- Matplotlib: rejected — static, no interactivity
- All-Plotly: rejected — violates Principle II (native-first mandate)

---

## 2. Filter State Management

**Decision**: Streamlit `st.session_state` for all filter values; sidebar controls write
to session state; `data.py` functions read filter values passed as arguments (not from
session state directly — keeps data functions pure and testable).

**Rationale**: Session state is Streamlit's canonical pattern for shared mutable state
across widget interactions. Passing filter values as function arguments (rather than
having `data.py` read session state) keeps `data.py` pure and independently testable
without a running Streamlit server — required by Constitution Principle III.

**Pattern**:
```
Sidebar widgets → st.session_state (date_range, categories, regions, granularity)
    ↓
app.py reads session_state values
    ↓
app.py calls data.py functions with explicit arguments
    ↓
data.py returns filtered/aggregated dataframes
    ↓
app.py calls charts.py with dataframes
    ↓
charts.py returns chart objects → rendered by app.py
```

**Alternatives considered**:
- Filter logic in `app.py` inline: rejected — untestable, violates Principle III
- `data.py` reads session_state: rejected — couples data module to Streamlit, breaks unit tests
- Third-party state management: rejected — violates Principle V (YAGNI)

---

## 3. Module Structure

**Decision**: Three modules — `app.py`, `data.py`, `charts.py`.

**Rationale**: Minimum split required for TDD compliance (Principle III). All data
loading, cleaning, filtering, and aggregation in `data.py`; chart construction in
`charts.py`; Streamlit UI wiring in `app.py`. Each module boundary maps to a testable
unit.

**Function inventory**:

`data.py`:
- `load_data(use_database: bool, connection_url: str | None) -> pd.DataFrame`
- `clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, int]` (returns cleaned df + excluded row count)
- `filter_data(df, date_range, categories, regions) -> pd.DataFrame`
- `compute_kpis(df: pd.DataFrame) -> dict`
- `aggregate_by_time(df, granularity: str) -> pd.DataFrame`
- `aggregate_by_column(df, column: str) -> pd.DataFrame`

`charts.py`:
- `build_trend_chart(df: pd.DataFrame) -> chart object`
- `build_bar_chart(df: pd.DataFrame, label_col: str, value_col: str, title: str) -> chart object`

**Alternatives considered**:
- Single `app.py`: rejected — data functions untestable without Streamlit server
- Four+ modules: rejected — Principle V (YAGNI); no current requirement justifies further split

---

## 4. Testing Strategy

**Decision**: Four-file test suite under `tests/`:

| File | Scope | TDD Required |
|------|-------|-------------|
| `test_data.py` | Unit tests for all `data.py` functions | Yes (Principle III) |
| `test_charts.py` | Unit tests for chart data-prep in `charts.py` | Yes (Principle III) |
| `test_integration.py` | Full pipeline with real `data/sales-data.csv` | Yes |
| `test_smoke.py` | Import `app.py`; no Streamlit server errors | Yes |

**Red-Green-Refactor cycle**: For each function in `data.py` and `charts.py`:
1. Write test → confirm FAIL
2. Implement minimum code → confirm PASS
3. Refactor → confirm still PASS

**Alternatives considered**:
- Data pipeline tests only: rejected — Principle III mandates full coverage including smoke
- UI rendering tests (Selenium/Playwright): rejected — not required by spec; manual verification sufficient per constitution

---

## 5. External Database Feature Flag

**Decision**: `USE_DATABASE` environment variable (true/false); when true, `DB_CONNECTION_URL` must also be set. SQLAlchemy used for DB path.

**Rationale**: Constitution Principle I requires external DB support. Feature flag
isolates the DB code path so Phase 1 CSV behaviour is unaffected. SQLAlchemy is the
minimal abstraction supporting Postgres, BigQuery (via connector), and SQLite with a
single interface.

**Behaviour**:
- `USE_DATABASE` absent or `false` → load from `data/sales-data.csv`
- `USE_DATABASE=true`, `DB_CONNECTION_URL` set → load via SQLAlchemy
- `USE_DATABASE=true`, `DB_CONNECTION_URL` absent → raise clear error with instructions
- DB connection failure → surface user-friendly error in Streamlit UI (not raw traceback)

**Streamlit Cloud deployment**: Both env vars set via Streamlit Cloud Secrets UI (not
committed to repo). CSV path requires no secrets.

**Alternatives considered**:
- Stub only (log warning, always use CSV): rejected — Principle I requires a real DB path
- Always-on SQLAlchemy (no feature flag): rejected — adds complexity to the CSV path; Principle V violation
- Database-only (drop CSV): rejected — contradicts Principle I (CSV as default)
