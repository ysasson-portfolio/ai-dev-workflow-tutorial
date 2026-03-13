"""
Unit tests for data.py — TDD suite for the ShopSmart Sales Analytics Dashboard.

Tests are organized by user story. Write tests first, confirm FAIL, then implement.

US1: load_data, clean_data, compute_kpis         (T010-T012)
US2: aggregate_by_time                            (T019-T021)
US3: aggregate_by_column                          (T029-T031)
US4: filter_data                                  (T039-T044)
"""
# clean_df monthly breakdown (from conftest):
#   Jan 2024: 99.98 + 19.99 = 119.97
#   Feb 2024: 239.97 + 199.99 = 439.96
#   Mar 2024: 79.98 + 119.96 = 199.94
#   Apr 2024: 89.99 + 99.98 = 189.97
#   May 2024: 399.99
from datetime import date

import pandas as pd
import pytest

import data


# ---------------------------------------------------------------------------
# US1 - KPI Scorecards (T010-T012)
# ---------------------------------------------------------------------------

def test_load_data_csv_returns_correct_shape():
    """T010: load_data() CSV path returns DataFrame with correct columns and rows."""
    df = data.load_data(use_database=False, connection_url=None)
    expected_columns = {"date", "order_id", "product", "category",
                        "region", "quantity", "unit_price", "total_amount"}
    assert set(df.columns) == expected_columns
    assert len(df) > 0


def test_clean_data_removes_null_rows(raw_df):
    """T011: clean_data() excludes rows with null total_amount, category, or region."""
    cleaned, excluded_count = data.clean_data(raw_df)
    # raw_df has row index 8 with null category AND null total_amount (same row)
    assert excluded_count == 1
    assert len(cleaned) == len(raw_df) - 1
    assert cleaned["total_amount"].notna().all()
    assert cleaned["category"].notna().all()
    assert cleaned["region"].notna().all()


def test_compute_kpis_correct_values(clean_df):
    """T012: compute_kpis() returns correct aggregated values from clean_df fixture."""
    kpis = data.compute_kpis(clean_df)
    assert kpis["total_sales"] == pytest.approx(1349.83, rel=1e-3)
    assert kpis["total_orders"] == 9
    assert kpis["avg_order_value"] == pytest.approx(1349.83 / 9, rel=1e-3)
    assert kpis["top_category"] == "Electronics"


def test_compute_kpis_empty_dataframe():
    """T012 edge case: compute_kpis() returns zero-safe values for empty DataFrame."""
    empty_df = pd.DataFrame(
        columns=["date", "order_id", "product", "category",
                 "region", "quantity", "unit_price", "total_amount"]
    )
    kpis = data.compute_kpis(empty_df)
    assert kpis["total_sales"] == 0.0
    assert kpis["total_orders"] == 0
    assert kpis["avg_order_value"] == 0.0
    assert kpis["top_category"] == "—"


# ---------------------------------------------------------------------------
# US2 - Sales Trend Over Time (T019-T021)
# ---------------------------------------------------------------------------

def test_aggregate_by_time_monthly(clean_df):
    """T019: aggregate_by_time() Monthly returns one row per calendar month."""
    result = data.aggregate_by_time(clean_df, "Monthly")
    assert list(result.columns) == ["period", "total_sales"]
    assert len(result) == 5  # Jan–May 2024
    periods = list(result["period"])
    assert periods == sorted(periods)  # ascending
    assert result.iloc[0]["period"] == date(2024, 1, 1)
    assert result.iloc[0]["total_sales"] == pytest.approx(119.97, rel=1e-3)
    assert result.iloc[1]["total_sales"] == pytest.approx(439.96, rel=1e-3)


def test_aggregate_by_time_daily(clean_df):
    """T020: aggregate_by_time() Daily returns one row per unique date, sorted ascending."""
    result = data.aggregate_by_time(clean_df, "Daily")
    assert list(result.columns) == ["period", "total_sales"]
    assert len(result) == 9  # 9 unique dates in clean_df
    periods = list(result["period"])
    assert periods == sorted(periods)  # ascending


def test_aggregate_by_time_invalid_granularity(clean_df):
    """T021: aggregate_by_time() raises ValueError for unknown granularity."""
    with pytest.raises(ValueError):
        data.aggregate_by_time(clean_df, "Weekly")
