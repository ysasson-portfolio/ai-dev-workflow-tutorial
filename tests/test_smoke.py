"""
Smoke tests for the ShopSmart Sales Analytics Dashboard.

Verifies that data and charts modules import cleanly and expose all
expected public functions. No business logic is tested here.
"""
import pytest


def test_data_module_imports():
    """T053: data module imports without errors."""
    import data  # noqa: F401


def test_charts_module_imports():
    """T053: charts module imports without errors."""
    import charts  # noqa: F401


def test_data_module_has_expected_functions():
    """T053: data module exposes all six public functions from the contract."""
    import data
    expected = {
        "load_data",
        "clean_data",
        "filter_data",
        "compute_kpis",
        "aggregate_by_time",
        "aggregate_by_column",
    }
    for fn in expected:
        assert hasattr(data, fn), f"data.{fn} is missing"
        assert callable(getattr(data, fn)), f"data.{fn} is not callable"


def test_charts_module_has_expected_functions():
    """T053: charts module exposes both public functions from the contract."""
    import charts
    expected = {"build_trend_chart", "build_bar_chart"}
    for fn in expected:
        assert hasattr(charts, fn), f"charts.{fn} is missing"
        assert callable(getattr(charts, fn)), f"charts.{fn} is not callable"
