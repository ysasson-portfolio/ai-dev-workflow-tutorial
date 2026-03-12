"""
data.py — Data loading, cleaning, filtering, and aggregation.

All functions are pure (no Streamlit imports, no side effects beyond I/O)
and are independently testable via pytest.

See specs/001-sales-dashboard/contracts/data-interface.md for full contracts.
"""
from __future__ import annotations

import os
from datetime import date

import pandas as pd


def load_data(use_database: bool, connection_url: str | None) -> pd.DataFrame:
    """Load raw transaction data from CSV or external database.

    Args:
        use_database: If True, load from connection_url via SQLAlchemy.
                      If False, load from data/sales-data.csv.
        connection_url: SQLAlchemy connection string (required when use_database=True).

    Returns:
        Raw DataFrame with Transaction schema columns.

    Raises:
        FileNotFoundError: CSV file missing or unreadable.
        ValueError: use_database=True but connection_url is None.
        ConnectionError: Database connection failed.
    """
    raise NotImplementedError


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove invalid rows and coerce types.

    Drops rows where total_amount, category, or region is null,
    where total_amount < 0, or where date is unparseable.

    Args:
        df: Raw DataFrame from load_data().

    Returns:
        Tuple of (cleaned DataFrame, count of excluded rows).
    """
    raise NotImplementedError


def filter_data(
    df: pd.DataFrame,
    date_start: date,
    date_end: date,
    categories: list[str],
    regions: list[str],
) -> pd.DataFrame:
    """Apply active filter state to a cleaned DataFrame.

    Args:
        df: Cleaned DataFrame from clean_data().
        date_start: Inclusive start date.
        date_end: Inclusive end date.
        categories: List of category values to include.
        regions: List of region values to include.

    Returns:
        Filtered DataFrame (empty DataFrame if no rows match, not an error).

    Raises:
        ValueError: If date_start > date_end.
    """
    raise NotImplementedError


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute the four KPI scalar values from a filtered DataFrame.

    Args:
        df: Filtered DataFrame from filter_data().

    Returns:
        Dict with keys: total_sales (float), total_orders (int),
        avg_order_value (float), top_category (str).
        Returns zero/empty-safe values when df is empty.
    """
    raise NotImplementedError


def aggregate_by_time(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    """Aggregate total sales by time period for the trend chart.

    Args:
        df: Filtered DataFrame from filter_data().
        granularity: "Monthly" or "Daily" (case-sensitive).

    Returns:
        DataFrame with columns ["period", "total_sales"],
        sorted ascending by period.

    Raises:
        ValueError: If granularity is not "Monthly" or "Daily".
    """
    raise NotImplementedError


def aggregate_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Aggregate total sales by a categorical column for bar charts.

    Args:
        df: Filtered DataFrame from filter_data().
        column: "category" or "region".

    Returns:
        DataFrame with columns ["label", "total_sales"],
        sorted descending by total_sales.

    Raises:
        ValueError: If column is not "category" or "region".
    """
    raise NotImplementedError
