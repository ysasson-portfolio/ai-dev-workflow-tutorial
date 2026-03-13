"""
Unit tests for charts.py — TDD suite for the ShopSmart Sales Analytics Dashboard.

Tests are organized by user story. Write tests first, confirm FAIL, then implement.

US2: build_trend_chart    (T022-T023)
US3: build_bar_chart      (T032-T033)
"""
import pandas as pd
import pytest

import charts
import data


# ---------------------------------------------------------------------------
# US2 - Sales Trend Chart (T022-T023)
# ---------------------------------------------------------------------------

def test_build_trend_chart_returns_chart(clean_df):
    """T022: build_trend_chart() returns a non-None chart object from valid data."""
    trend_df = data.aggregate_by_time(clean_df, "Monthly")
    chart = charts.build_trend_chart(trend_df)
    assert chart is not None


def test_build_trend_chart_empty_dataframe():
    """T023: build_trend_chart() returns without error when DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["period", "total_sales"])
    chart = charts.build_trend_chart(empty_df)
    assert chart is not None


# ---------------------------------------------------------------------------
# US3 - Bar Charts (T032-T033)
# ---------------------------------------------------------------------------

def test_build_bar_chart_returns_chart(clean_df):
    """T032: build_bar_chart() returns a non-None chart object from valid data."""
    bar_df = data.aggregate_by_column(clean_df, "category")
    chart = charts.build_bar_chart(bar_df, "label", "total_sales", "Sales by Category")
    assert chart is not None


def test_build_bar_chart_empty_dataframe():
    """T033: build_bar_chart() returns without error when DataFrame is empty."""
    empty_df = pd.DataFrame(columns=["label", "total_sales"])
    chart = charts.build_bar_chart(empty_df, "label", "total_sales", "Sales by Category")
    assert chart is not None
