"""
app.py — ShopSmart Sales Analytics Dashboard.

Streamlit entry point. Handles page config, sidebar filters, session state
initialisation, layout, and chart rendering. All data logic lives in data.py;
all chart construction lives in charts.py.
"""
import streamlit as st

import charts
import data

# ---------------------------------------------------------------------------
# Page config (FR-021)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
try:
    _raw_df = data.load_data(use_database=False, connection_url=None)
    _df, _excluded = data.clean_data(_raw_df)
except Exception as _e:
    st.error(f"Failed to load data: {_e}")
    st.stop()


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
# TODO T047: initialise st.session_state defaults
# (date_start, date_end, selected_categories, selected_regions, granularity)


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
# TODO T048: add st.sidebar controls (date_input, multiselect × 2)


# ---------------------------------------------------------------------------
# Filtered data
# ---------------------------------------------------------------------------
# TODO T049: call data.filter_data() with session_state values
_filtered_df = _df


# ---------------------------------------------------------------------------
# KPI scorecards  (US1)
# ---------------------------------------------------------------------------
_kpis = data.compute_kpis(_filtered_df)
_col1, _col2, _col3, _col4 = st.columns(4)
_col1.metric("Total Sales", f"${_kpis['total_sales']:,.2f}")
_col2.metric("Total Orders", f"{_kpis['total_orders']:,}")
_col3.metric("Avg Order Value", f"${_kpis['avg_order_value']:,.2f}")
_col4.metric("Top Category", _kpis["top_category"])


# ---------------------------------------------------------------------------
# Sales trend chart  (US2)
# ---------------------------------------------------------------------------
st.subheader("Sales Trend")
# Using st.plotly_chart: build_trend_chart() returns a Plotly Figure because
# st.line_chart does not support custom y-axis labels ("Sales ($)") natively.
_granularity = st.radio("Granularity", ["Monthly", "Daily"], horizontal=True)
_trend_df = data.aggregate_by_time(_filtered_df, _granularity)
st.plotly_chart(charts.build_trend_chart(_trend_df), use_container_width=True)


# ---------------------------------------------------------------------------
# Category and region bar charts  (US3)
# ---------------------------------------------------------------------------
# TODO T037: two-column layout with aggregate_by_column() + build_bar_chart()
