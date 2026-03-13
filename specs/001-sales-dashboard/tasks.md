# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `/specs/001-sales-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD required for `data.py` and `charts.py` per Constitution Principle III.
Test tasks are grouped at the top of each user story phase (tests-first per phase).

**Organization**: Tasks grouped by user story. P1+P2+P3 = MVP. P4 (filtering) added last.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in all implementation task descriptions

---

## Phase 1: Setup

**Purpose**: Project initialization — stubs, dependencies, test scaffolding

- [x] T001 Initialize `pyproject.toml` with all dependencies via `uv add streamlit plotly pandas sqlalchemy pytest`
- [x] T002 Create `data.py` with all function stubs (empty bodies, correct signatures) matching `specs/001-sales-dashboard/contracts/data-interface.md`
- [x] T003 [P] Create `charts.py` with all function stubs matching `specs/001-sales-dashboard/contracts/charts-interface.md`
- [x] T004 [P] Create `app.py` with Streamlit imports, page config stub, and section placeholder comments
- [x] T005 [P] Create `tests/` directory with empty `tests/test_data.py`, `tests/test_charts.py`, `tests/test_integration.py`, `tests/test_smoke.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure that MUST be complete before any user story begins

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Manually verify `data/sales-data.csv` loads in a Python REPL: confirm 8 columns (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`) and ~1,000 rows
- [x] T007 [P] Configure pytest in `pyproject.toml` under `[tool.pytest.ini_options]` (testpaths = `["tests"]`, verbose output)
- [x] T008 [P] Create `tests/conftest.py` with shared fixtures: a sample raw DataFrame (10 rows) and a sample cleaned DataFrame matching the Transaction schema in `specs/001-sales-dashboard/data-model.md`
- [x] T009 Set page config in `app.py`: `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and `st.title("ShopSmart Sales Dashboard")` (FR-021)

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — View KPI Scorecards (Priority: P1) 🎯 MVP Start

**Goal**: Four KPI metric cards (Total Sales, Total Orders, Average Order Value, Top
Category) visible on page load with correct values from `data/sales-data.csv`.

**Independent Test**: Open dashboard, verify four `st.metric` cards are visible and
values match manual CSV calculations (Total Sales ≈ $650K–$700K, Total Orders = 482).

### Tests for User Story 1 (TDD — write first, confirm FAIL before implementing)

- [x] T010 [P] [US1] Write test `test_load_data_csv_returns_correct_shape` in `tests/test_data.py`: assert DataFrame has 8 expected columns and row count > 0
- [x] T011 [P] [US1] Write test `test_clean_data_removes_null_rows` in `tests/test_data.py`: inject rows with null `total_amount`/`category`/`region`; assert excluded_count matches injected nulls
- [x] T012 [P] [US1] Write test `test_compute_kpis_correct_values` in `tests/test_data.py`: use conftest fixture; assert `total_sales`, `total_orders`, `avg_order_value`, `top_category` match expected values
- [x] T013 [US1] Confirm T010–T012 FAIL: run `uv run pytest tests/test_data.py -v` and verify all three tests show FAILED before proceeding

### Implementation for User Story 1

- [x] T014 [US1] Implement `load_data()` CSV path in `data.py`: read `data/sales-data.csv` with `pd.read_csv`, parse `date` column, raise `FileNotFoundError` with descriptive message if missing
- [x] T015 [US1] Implement `clean_data()` in `data.py`: drop rows where `total_amount`, `category`, or `region` is null or `total_amount` < 0; return `(cleaned_df, excluded_count)`
- [x] T016 [US1] Implement `compute_kpis()` in `data.py`: compute `total_sales`, `total_orders` (unique `order_id`), `avg_order_value`, `top_category`; return empty-safe dict when DataFrame is empty
- [x] T017 [US1] Render four KPI scorecards in `app.py` using `st.metric()` in a four-column layout: Total Sales ($), Total Orders, Average Order Value ($), Top Category
- [x] T018 [US1] Confirm T010–T012 PASS: run `uv run pytest tests/test_data.py -v` and verify all three tests show PASSED

**Checkpoint**: US1 complete — KPI scorecards independently functional and tested

---

## Phase 4: User Story 2 — Explore Sales Trend Over Time (Priority: P2)

**Goal**: Line chart showing sales over time with Daily/Monthly granularity toggle,
defaulting to Monthly.

**Independent Test**: Verify line chart renders with labeled axes; toggle between Daily
and Monthly; confirm chart updates with correct number of data points for each.

### Tests for User Story 2 (TDD — write first, confirm FAIL before implementing)

- [x] T019 [P] [US2] Write test `test_aggregate_by_time_monthly` in `tests/test_data.py`: assert output has one row per calendar month with correct `period` and `total_sales` values
- [x] T020 [P] [US2] Write test `test_aggregate_by_time_daily` in `tests/test_data.py`: assert output has one row per unique date, sorted ascending
- [x] T021 [P] [US2] Write test `test_aggregate_by_time_invalid_granularity` in `tests/test_data.py`: assert `ValueError` raised for unknown granularity string
- [x] T022 [P] [US2] Write test `test_build_trend_chart_returns_chart` in `tests/test_charts.py`: assert non-None return from valid time-series DataFrame
- [x] T023 [P] [US2] Write test `test_build_trend_chart_empty_dataframe` in `tests/test_charts.py`: assert function returns without error when DataFrame is empty
- [x] T024 [US2] Confirm T019–T023 FAIL: run `uv run pytest tests/test_data.py tests/test_charts.py -v` and verify all five tests show FAILED

### Implementation for User Story 2

- [x] T025 [US2] Implement `aggregate_by_time()` in `data.py`: group by month-start (Monthly) or date (Daily), sum `total_amount`, sort ascending by `period`, return DataFrame with columns `["period", "total_sales"]`
- [x] T026 [US2] Implement `build_trend_chart()` in `charts.py`: use `st.line_chart`-compatible DataFrame; fall back to Plotly only if axis labelling requires it (document reason in `app.py` call site comment)
- [x] T027 [US2] Add trend chart section to `app.py`: `st.radio` granularity toggle (options: `["Monthly", "Daily"]`, default `"Monthly"`), call `aggregate_by_time()` and `build_trend_chart()`, render chart with `st.line_chart` or `st.plotly_chart`
- [x] T028 [US2] Confirm T019–T023 PASS: run `uv run pytest tests/test_data.py tests/test_charts.py -v`

**Checkpoint**: US2 complete — trend chart independently functional and tested

---

## Phase 5: User Story 3 — Analyse Sales by Category and Region (Priority: P3) 🎯 MVP Complete

**Goal**: Two bar charts side-by-side — Sales by Category and Sales by Region — both
sorted descending.

**Independent Test**: Verify two bar charts render; confirm bars are sorted highest to
lowest; hover tooltip shows segment name and exact value.

### Tests for User Story 3 (TDD — write first, confirm FAIL before implementing)

- [x] T029 [P] [US3] Write test `test_aggregate_by_column_category_sorted` in `tests/test_data.py`: assert output is sorted descending by `total_sales` and `label` column contains category values
- [x] T030 [P] [US3] Write test `test_aggregate_by_column_region_sorted` in `tests/test_data.py`: assert output is sorted descending and `label` column contains region values
- [x] T031 [P] [US3] Write test `test_aggregate_by_column_invalid_column` in `tests/test_data.py`: assert `ValueError` raised for column name not in `["category", "region"]`
- [x] T032 [P] [US3] Write test `test_build_bar_chart_returns_chart` in `tests/test_charts.py`: assert non-None return from valid segment DataFrame
- [x] T033 [P] [US3] Write test `test_build_bar_chart_empty_dataframe` in `tests/test_charts.py`: assert function returns without error when DataFrame is empty
- [x] T034 [US3] Confirm T029–T033 FAIL: run `uv run pytest tests/test_data.py tests/test_charts.py -v` and verify all five tests show FAILED

### Implementation for User Story 3

- [x] T035 [US3] Implement `aggregate_by_column()` in `data.py`: group by `category` or `region`, sum `total_amount`, rename columns to `["label", "total_sales"]`, sort descending
- [x] T036 [US3] Implement `build_bar_chart()` in `charts.py`: use `st.bar_chart`-compatible DataFrame; fall back to Plotly only if descending-sort display requires it (document reason in `app.py` call site comment)
- [x] T037 [US3] Add category and region bar charts to `app.py` in a two-column layout using `st.columns(2)`: call `aggregate_by_column()` and `build_bar_chart()` for each segment
- [x] T038 [US3] Confirm T029–T033 PASS; run full dashboard locally (`uv run streamlit run app.py`) and validate MVP: all four KPIs, trend chart, and both bar charts visible and correct

**Checkpoint**: MVP complete — US1 + US2 + US3 fully functional and independently testable

---

## Phase 6: User Story 4 — Filter Dashboard by Date, Category, and Region (Priority: P4)

**Goal**: Sidebar with date range picker, category multi-select, and region multi-select;
all charts and KPIs update immediately when any filter changes via `st.session_state`.

**Independent Test**: Set date range to Q1 only; verify all four KPIs, trend chart, and
both bar charts show only Q1 data. Add "Electronics" category filter; verify all views
narrow further.

### Tests for User Story 4 (TDD — write first, confirm FAIL before implementing)

- [ ] T039 [P] [US4] Write test `test_filter_data_date_range_inclusive` in `tests/test_data.py`: assert rows outside date range are excluded; boundary dates are included
- [ ] T040 [P] [US4] Write test `test_filter_data_category_filter` in `tests/test_data.py`: assert only rows matching selected categories are returned
- [ ] T041 [P] [US4] Write test `test_filter_data_region_filter` in `tests/test_data.py`: assert only rows matching selected regions are returned
- [ ] T042 [P] [US4] Write test `test_filter_data_combined_filters` in `tests/test_data.py`: assert combined date + category + region filters apply correctly
- [ ] T043 [P] [US4] Write test `test_filter_data_empty_result` in `tests/test_data.py`: assert empty DataFrame returned (not error) when no rows match filter
- [ ] T044 [P] [US4] Write test `test_filter_data_invalid_date_range` in `tests/test_data.py`: assert `ValueError` raised when `date_start > date_end`
- [ ] T045 [US4] Confirm T039–T044 FAIL: run `uv run pytest tests/test_data.py -v` and verify all six tests show FAILED

### Implementation for User Story 4

- [ ] T046 [US4] Implement `filter_data()` in `data.py`: filter by inclusive date range, category list, and region list; raise `ValueError` when `date_start > date_end`; return empty DataFrame (not error) when no rows match
- [ ] T047 [US4] Initialise `st.session_state` defaults in `app.py` (at page top, before sidebar): `date_start`, `date_end` (from data min/max), `selected_categories` (all), `selected_regions` (all), `granularity` ("Monthly")
- [ ] T048 [US4] Add sidebar filter controls to `app.py` using `st.sidebar`: `st.date_input` for date range, `st.multiselect` for categories, `st.multiselect` for regions; write selected values to `st.session_state`
- [ ] T049 [US4] Refactor `app.py` to pass `st.session_state` filter values to `filter_data()` before all aggregation calls; confirm all chart and KPI sections use the filtered DataFrame
- [ ] T050 [US4] Refactor granularity toggle in `app.py` to read/write `st.session_state.granularity` so filter state and granularity are consistent across re-renders
- [ ] T051 [US4] Confirm T039–T044 PASS: run `uv run pytest tests/test_data.py -v`

**Checkpoint**: US4 complete — all four user stories independently functional and tested

---

## Phase 7: Integration & Smoke Tests

**Purpose**: End-to-end pipeline validation and app import verification

- [ ] T052 [P] Write integration test in `tests/test_integration.py`: run full pipeline `load_data()` → `clean_data()` → `filter_data()` → `compute_kpis()` with real `data/sales-data.csv`; assert Total Orders = 482 and Total Sales is within $650K–$700K
- [ ] T053 [P] Write smoke test in `tests/test_smoke.py`: import `data` and `charts` modules; assert no import errors; verify all expected function names are present
- [ ] T054 Run full pytest suite (`uv run pytest tests/ -v`) and confirm all tests pass across all four files

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, DB feature flag, performance validation, documentation

- [ ] T055 Implement empty-state guard in `app.py`: before rendering any chart, check if filtered DataFrame is empty; display `st.info("No data for selected filters.")` and skip chart rendering
- [ ] T056 [P] Implement user-friendly error handling in `app.py`: wrap `load_data()` + `clean_data()` in a try/except block; display `st.error("Could not load sales data: {message}")` on failure instead of traceback
- [ ] T057 [P] Implement `USE_DATABASE` feature flag in `data.py` `load_data()`: read `USE_DATABASE` env var; if `"true"`, load from `DB_CONNECTION_URL` via SQLAlchemy `pd.read_sql()`; raise `ValueError` if `DB_CONNECTION_URL` is absent; raise `ConnectionError` on DB failure
- [ ] T058 [P] Implement null-row warning in `app.py`: display `st.warning(f"{excluded_count} row(s) excluded due to missing data.")` when `excluded_count > 0` from `clean_data()`
- [ ] T059 Manual timing check: load dashboard locally and verify full page load ≤ 5 s (SC-001); apply a filter and verify re-render ≤ 2 s (SC-004); note any issues
- [ ] T060 Run quickstart.md validation checklist (`specs/001-sales-dashboard/quickstart.md`) manually and confirm all items checked
- [ ] T061 Create `README.md` at repo root with: local setup steps, `uv run streamlit run app.py` command, environment variable reference (`USE_DATABASE`, `DB_CONNECTION_URL`), and Streamlit Community Cloud deploy steps
- [ ] T062 Run final `uv run pytest tests/ -v` and confirm all tests still pass after all polish changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2
- **US2 (Phase 4)**: Depends on Phase 2; may start after US1 (shares `data.py`)
- **US3 (Phase 5)**: Depends on Phase 2; may start after US1 (shares `data.py`)
- **US4 (Phase 6)**: Depends on US1 (needs `load_data` + `clean_data`); best started after US1–US3
- **Integration (Phase 7)**: Depends on US1–US4 complete
- **Polish (Phase 8)**: Depends on Phase 7

### User Story Dependencies

- **US1 (P1)**: After Foundational — no story dependencies
- **US2 (P2)**: After Foundational — independent of US1 but shares `data.py` stubs
- **US3 (P3)**: After Foundational — independent of US1/US2 but shares `data.py` stubs
- **US4 (P4)**: After US1 (requires working `load_data` + `clean_data`); integrates with US2/US3 for wiring

### Within Each User Story

- All `[P]` test tasks can be written in parallel (different test functions, same file is fine)
- Tests MUST be written and FAIL before implementation begins
- Implementation tasks proceed sequentially: data.py → charts.py → app.py wiring
- Story complete when tests PASS

---

## Parallel Opportunities

```bash
# Phase 1 — run T002, T003, T004, T005 in parallel:
Task: "Create data.py stubs"
Task: "Create charts.py stubs"
Task: "Create app.py stub"
Task: "Create tests/ scaffolding"

# Phase 3 (US1) — write all three tests in parallel:
Task: "test_load_data_csv_returns_correct_shape"
Task: "test_clean_data_removes_null_rows"
Task: "test_compute_kpis_correct_values"

# Phase 8 — run T056, T057, T058 in parallel:
Task: "CSV error handling in app.py"
Task: "USE_DATABASE feature flag in data.py"
Task: "Null-row warning in app.py"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (**CRITICAL — blocks all stories**)
3. Complete Phase 3: US1 (KPI scorecards) → validate independently
4. Complete Phase 4: US2 (trend chart) → validate independently
5. Complete Phase 5: US3 (bar charts) → **STOP and validate MVP**
6. Deploy/demo MVP before proceeding to US4

### Incremental Delivery

1. Setup + Foundational → ready to build
2. US1 → test → demo (KPI scorecards)
3. US2 → test → demo (+ trend chart)
4. US3 → test → demo (full MVP — 3 chart types)
5. US4 → test → demo (+ filters)
6. Integration + Polish → production-ready

---

## Notes

- `[P]` = parallelizable (no dependency on incomplete tasks in same phase)
- TDD cycle per function: write test → confirm FAIL → implement → confirm PASS → refactor
- Commit after each "Confirm PASS" checkpoint with Jira issue key prefix (e.g., `ECOM-1: ...`)
- All `data.py` functions MUST remain pure (no `st.*` imports) to stay testable
- Plotly use in `charts.py` MUST be justified with a comment in the `app.py` call site
