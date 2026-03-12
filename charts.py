"""
charts.py — Chart builder functions for the ShopSmart Sales Dashboard.

All functions accept pre-aggregated DataFrames (from data.py) and return
chart objects for rendering by app.py. No st.* calls are made here.

See specs/001-sales-dashboard/contracts/charts-interface.md for full contracts.
"""
from __future__ import annotations

import pandas as pd


def build_trend_chart(df: pd.DataFrame):
    """Build the sales trend line chart from a time-aggregated DataFrame.

    Prefers st.line_chart-compatible format (indexed DataFrame).
    Falls back to Plotly only if axis labelling cannot be achieved natively
    — justify the fallback in the app.py call site comment.

    Args:
        df: DataFrame with columns ["period", "total_sales"],
            output of data.aggregate_by_time().

    Returns:
        A Streamlit-compatible chart object, or an indexed DataFrame
        for use with st.line_chart(). Returns an empty DataFrame
        (not an error) when input is empty.
    """
    raise NotImplementedError


def build_bar_chart(
    df: pd.DataFrame,
    label_col: str,
    value_col: str,
    title: str,
):
    """Build a sorted bar chart for category/region segment breakdowns.

    Input DataFrame is already sorted descending by value_col (done by
    data.aggregate_by_column). This function MUST NOT re-sort.

    Prefers st.bar_chart-compatible format. Falls back to Plotly only if
    descending-sort display cannot be achieved natively — justify in app.py.

    Args:
        df: DataFrame with columns [label_col, value_col], sorted descending.
        label_col: Column name for segment labels (e.g. "label").
        value_col: Column name for sales values (e.g. "total_sales").
        title: Chart title string.

    Returns:
        A Streamlit-compatible chart object, or a chart-ready DataFrame.
        Returns an empty DataFrame (not an error) when input is empty.
    """
    raise NotImplementedError
