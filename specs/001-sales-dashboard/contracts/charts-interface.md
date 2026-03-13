# Contract: charts.py Public Interface

**Module**: `charts.py`
**Date**: 2026-03-12

This module contains pure chart-builder functions. Each function accepts a pre-aggregated
DataFrame (from `data.py`) and returns a chart object suitable for rendering in Streamlit.
No Streamlit rendering calls (`st.*`) are made inside this module — that is `app.py`'s
responsibility.

---

## build_trend_chart

```
build_trend_chart(df: pd.DataFrame) -> chart object
```

**Purpose**: Build the sales trend line chart from a time-aggregated DataFrame.

**Input**: DataFrame with columns `["period", "total_sales"]` (output of
`data.aggregate_by_time()`).

**Output**: A Streamlit-compatible chart object.
- Prefer `st.line_chart`-compatible format (indexed DataFrame).
- Use Plotly (`plotly.graph_objects.Figure`) only if tooltip customisation or axis
  labelling cannot be achieved natively. If Plotly is used, the call site in `app.py`
  MUST include a comment explaining why.

**Requirements**:
- x-axis: `period` (time)
- y-axis: `total_sales` (labelled "Sales ($)")
- Interactive tooltip showing period label and exact sales value
- Returns empty/blank chart (not error) when input DataFrame is empty

---

## build_bar_chart

```
build_bar_chart(
    df: pd.DataFrame,
    label_col: str,
    value_col: str,
    title: str,
) -> chart object
```

**Purpose**: Build a sorted horizontal or vertical bar chart for category/region breakdown.

**Input**: DataFrame with columns `[label_col, value_col]` (output of
`data.aggregate_by_column()`), already sorted descending by `value_col`.

**Output**: A Streamlit-compatible chart object.
- Prefer `st.bar_chart`-compatible format.
- Use Plotly only if descending sort display or tooltip customisation cannot be achieved
  natively. Justify in `app.py` call site comment if Plotly is used.

**Requirements**:
- Bars sorted descending by `value_col` (sort is applied by `data.aggregate_by_column`
  before this function is called — charts.py MUST NOT re-sort)
- Chart title displayed (passed as `title` argument)
- x-axis / y-axis labelled
- Interactive tooltip showing segment name and exact sales value
- Returns empty/blank chart (not error) when input DataFrame is empty
