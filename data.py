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
    if use_database:
        if connection_url is None:
            raise ValueError("connection_url is required when use_database=True")
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(connection_url)
            with engine.connect() as conn:
                return pd.read_sql(text("SELECT * FROM transactions"), conn)
        except Exception as exc:
            raise ConnectionError(f"Database connection failed: {exc}") from exc

    csv_path = os.path.join(os.path.dirname(__file__), "data", "sales-data.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return pd.read_csv(csv_path)


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove invalid rows and coerce types.

    Drops rows where total_amount, category, or region is null,
    where total_amount < 0, or where date is unparseable.

    Args:
        df: Raw DataFrame from load_data().

    Returns:
        Tuple of (cleaned DataFrame, count of excluded rows).
    """
    original_len = len(df)
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    mask = (
        df["total_amount"].notna()
        & df["category"].notna()
        & df["region"].notna()
        & (df["total_amount"] >= 0)
        & df["date"].notna()
    )
    cleaned = df[mask].copy()
    cleaned["date"] = cleaned["date"].dt.date
    excluded_count = original_len - len(cleaned)
    return cleaned, excluded_count


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
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_orders": 0,
            "avg_order_value": 0.0,
            "top_category": "—",
        }
    total_sales = float(df["total_amount"].sum())
    total_orders = int(df["order_id"].nunique())
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    top_category = df.groupby("category")["total_amount"].sum().idxmax()
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "top_category": top_category,
    }


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
    if granularity not in ("Monthly", "Daily"):
        raise ValueError(f"granularity must be 'Monthly' or 'Daily', got {granularity!r}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    if granularity == "Monthly":
        df["period"] = df["date"].dt.to_period("M").dt.to_timestamp().dt.date
    else:
        df["period"] = df["date"].dt.date

    result = (
        df.groupby("period", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("period")
        .reset_index(drop=True)
    )
    return result[["period", "total_sales"]]


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
