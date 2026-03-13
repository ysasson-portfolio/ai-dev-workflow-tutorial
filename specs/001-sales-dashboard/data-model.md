# Data Model: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-12

---

## Source Schema: Transaction

Loaded from `data/sales-data.csv` (or external DB table with identical schema).

| Field | Type | Description | Example | Nullable |
|-------|------|-------------|---------|----------|
| `date` | date (ISO 8601) | Transaction date | 2024-01-15 | No |
| `order_id` | string | Unique order identifier | ORD-001234 | No |
| `product` | string | Product name | Wireless Headphones | No |
| `category` | string | Product category | Electronics | No — excluded if null |
| `region` | string | Geographic region | North | No — excluded if null |
| `quantity` | integer | Units sold | 2 | No |
| `unit_price` | decimal | Price per unit | 49.99 | No |
| `total_amount` | decimal | Total transaction value | 99.98 | No — excluded if null |

**Validation rules**:
- Rows where `total_amount`, `category`, or `region` is null MUST be dropped before any
  aggregation. The count of dropped rows is surfaced as a UI warning (FR-020).
- `date` must be parseable as `YYYY-MM-DD`. Unparseable dates are treated as null and
  the row is excluded.
- `total_amount` must be ≥ 0. Negative values are treated as data errors and excluded.

**Known values** (from PRD):
- Categories: Electronics, Accessories, Audio, Wearables, Smart Home (5 total)
- Regions: North, South, East, West (4 total)
- ~1,000 rows; 12 months of data

---

## Derived Entity: Filter State

Held in `st.session_state`. Passed explicitly to `data.py` functions as arguments.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `date_start` | date | min date in dataset | Start of active date filter |
| `date_end` | date | max date in dataset | End of active date filter |
| `selected_categories` | list[str] | all categories | Active category filter |
| `selected_regions` | list[str] | all regions | Active region filter |
| `granularity` | str (`"Monthly"` \| `"Daily"`) | `"Monthly"` | Trend chart time granularity |

---

## Derived Entity: KPI Set

Computed by `data.compute_kpis(df)` from a filtered Transaction dataframe.

| Field | Type | Computation | Display Format |
|-------|------|-------------|----------------|
| `total_sales` | float | `sum(total_amount)` | `$X,XXX,XXX` |
| `total_orders` | int | `nunique(order_id)` | Integer with comma separator |
| `avg_order_value` | float | `total_sales / total_orders` | `$X,XXX` |
| `top_category` | str | `category` with max `sum(total_amount)` | String label |

**Edge case**: If the filtered dataframe is empty, all KPI values return 0 / `"—"`.

---

## Derived Entity: Time Series (Trend Chart Data)

Computed by `data.aggregate_by_time(df, granularity)`.

| Field | Type | Description |
|-------|------|-------------|
| `period` | date | Month start (Monthly) or transaction date (Daily) |
| `total_sales` | float | Sum of `total_amount` for the period |

**Aggregation**:
- Monthly: group by `date.dt.to_period('M')`, sum `total_amount`
- Daily: group by `date`, sum `total_amount`

---

## Derived Entity: Segment Breakdown (Bar Chart Data)

Computed by `data.aggregate_by_column(df, column)` where `column` is `"category"` or
`"region"`.

| Field | Type | Description |
|-------|------|-------------|
| `label` | str | Category or region name |
| `total_sales` | float | Sum of `total_amount` for the segment |

**Sorting**: Descending by `total_sales` (FR-009, FR-010).

---

## Data Flow

```
CSV / DB
    │
    ▼
load_data()          → raw DataFrame (all columns, original types)
    │
    ▼
clean_data()         → (cleaned DataFrame, excluded_row_count)
    │
    ▼  [Filter State applied]
filter_data()        → filtered DataFrame
    │
    ├──► compute_kpis()          → KPI dict  → st.metric() × 4
    ├──► aggregate_by_time()     → time series DataFrame → trend chart
    ├──► aggregate_by_column("category") → segment DataFrame → category bar chart
    └──► aggregate_by_column("region")   → segment DataFrame → region bar chart
```
