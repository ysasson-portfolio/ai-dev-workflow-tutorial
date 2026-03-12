# Contract: data.py Public Interface

**Module**: `data.py`
**Date**: 2026-03-12

This module is the single source of truth for data loading, cleaning, filtering, and
aggregation. All functions are pure (no Streamlit imports, no side effects beyond I/O)
and must be independently testable via pytest.

---

## load_data

```
load_data(use_database: bool, connection_url: str | None) -> pd.DataFrame
```

**Purpose**: Load raw transaction data from CSV or external database.

**Inputs**:
- `use_database`: if `True`, load from `connection_url`; if `False`, load from `data/sales-data.csv`
- `connection_url`: SQLAlchemy connection string (required when `use_database=True`)

**Output**: Raw DataFrame with columns matching the Transaction schema.

**Errors**:
- CSV missing/unreadable → raises `FileNotFoundError` with descriptive message
- `use_database=True` and `connection_url=None` → raises `ValueError`
- DB connection failure → raises `ConnectionError` with descriptive message

---

## clean_data

```
clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, int]
```

**Purpose**: Remove invalid rows and coerce types.

**Rules**:
- Drop rows where `total_amount`, `category`, or `region` is null
- Drop rows where `total_amount` < 0
- Drop rows where `date` is not parseable as `YYYY-MM-DD`
- Parse `date` column to `datetime.date`

**Output**: `(cleaned_df, excluded_count)` — cleaned DataFrame and count of dropped rows.

---

## filter_data

```
filter_data(
    df: pd.DataFrame,
    date_start: date,
    date_end: date,
    categories: list[str],
    regions: list[str],
) -> pd.DataFrame
```

**Purpose**: Apply active filter state to a cleaned DataFrame.

**Rules**:
- Include only rows where `date` is between `date_start` and `date_end` (inclusive)
- Include only rows where `category` is in `categories`
- Include only rows where `region` is in `regions`
- Returns empty DataFrame (not error) if no rows match

**Validation**:
- `date_start > date_end` → raises `ValueError("date_start must be ≤ date_end")`

---

## compute_kpis

```
compute_kpis(df: pd.DataFrame) -> dict
```

**Purpose**: Compute the four KPI scalar values from a filtered DataFrame.

**Output**:
```python
{
    "total_sales": float,        # sum of total_amount
    "total_orders": int,         # nunique of order_id
    "avg_order_value": float,    # total_sales / total_orders (0.0 if total_orders == 0)
    "top_category": str,         # category with highest sum(total_amount) ("—" if empty)
}
```

**Edge case**: Empty DataFrame → returns `{"total_sales": 0.0, "total_orders": 0, "avg_order_value": 0.0, "top_category": "—"}`.

---

## aggregate_by_time

```
aggregate_by_time(df: pd.DataFrame, granularity: str) -> pd.DataFrame
```

**Purpose**: Aggregate total sales by time period for the trend chart.

**Inputs**:
- `granularity`: `"Monthly"` or `"Daily"` (case-sensitive)

**Output**: DataFrame with columns `["period", "total_sales"]`, sorted ascending by `period`.

- Monthly: `period` is the first day of each month (`datetime.date`)
- Daily: `period` is the transaction date (`datetime.date`)

**Errors**: Invalid `granularity` value → raises `ValueError`.

---

## aggregate_by_column

```
aggregate_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame
```

**Purpose**: Aggregate total sales by a categorical column for bar charts.

**Inputs**:
- `column`: `"category"` or `"region"`

**Output**: DataFrame with columns `["label", "total_sales"]`, sorted **descending** by `total_sales`.

**Errors**: `column` not in `["category", "region"]` → raises `ValueError`.
