"""
Unit tests for data.py — TDD suite for the ShopSmart Sales Analytics Dashboard.

Tests are organized by user story. Write tests first, confirm FAIL, then implement.

US1: load_data, clean_data, compute_kpis         (T010-T012)
US2: aggregate_by_time                            (T019-T021)
US3: aggregate_by_column                          (T029-T031)
US4: filter_data                                  (T039-T044)
"""
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
