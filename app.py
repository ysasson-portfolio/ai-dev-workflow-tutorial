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
# TODO T014 / T056: load and clean data; display error on failure


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


# ---------------------------------------------------------------------------
# KPI scorecards  (US1)
# ---------------------------------------------------------------------------
# TODO T017: render four st.metric() cards in a 4-column layout


# ---------------------------------------------------------------------------
# Sales trend chart  (US2)
# ---------------------------------------------------------------------------
# TODO T027: granularity radio + aggregate_by_time() + build_trend_chart()


# ---------------------------------------------------------------------------
# Category and region bar charts  (US3)
# ---------------------------------------------------------------------------
# TODO T037: two-column layout with aggregate_by_column() + build_bar_chart()
