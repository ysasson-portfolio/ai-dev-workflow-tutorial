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
# Data loading  (T056 — USE_DATABASE feature flag, user-friendly error)
# ---------------------------------------------------------------------------
import os as _os
_use_db = _os.environ.get("USE_DATABASE", "false").lower() == "true"
_db_url = _os.environ.get("DB_CONNECTION_URL", None)

try:
    _raw_df = data.load_data(use_database=_use_db, connection_url=_db_url)
    _df, _excluded = data.clean_data(_raw_df)
except Exception as _e:
    st.error(f"Could not load sales data: {_e}")
    st.stop()


# T058 — null-row warning
if _excluded > 0:
    st.warning(f"{_excluded} row(s) excluded due to missing data.")


# ---------------------------------------------------------------------------
# Session state initialisation  (T047)
# ---------------------------------------------------------------------------
_all_categories = sorted(_df["category"].unique().tolist())
_all_regions = sorted(_df["region"].unique().tolist())
_date_min = _df["date"].min() if hasattr(_df["date"].min(), "year") else pd.to_datetime(_df["date"]).dt.date.min()
_date_max = _df["date"].max() if hasattr(_df["date"].max(), "year") else pd.to_datetime(_df["date"]).dt.date.max()

if "date_start" not in st.session_state:
    st.session_state.date_start = _date_min
if "date_end" not in st.session_state:
    st.session_state.date_end = _date_max
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = _all_categories
if "selected_regions" not in st.session_state:
    st.session_state.selected_regions = _all_regions
if "granularity" not in st.session_state:
    st.session_state.granularity = "Monthly"


# ---------------------------------------------------------------------------
# Sidebar filters  (T048)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")
    _date_range = st.date_input(
        "Date Range",
        value=(st.session_state.date_start, st.session_state.date_end),
        min_value=_date_min,
        max_value=_date_max,
    )
    if isinstance(_date_range, (list, tuple)) and len(_date_range) == 2:
        st.session_state.date_start = _date_range[0]
        st.session_state.date_end = _date_range[1]

    st.session_state.selected_categories = st.multiselect(
        "Categories",
        options=_all_categories,
        default=st.session_state.selected_categories,
    )
    st.session_state.selected_regions = st.multiselect(
        "Regions",
        options=_all_regions,
        default=st.session_state.selected_regions,
    )


# ---------------------------------------------------------------------------
# Filtered data  (T049)
# ---------------------------------------------------------------------------
_filtered_df = data.filter_data(
    _df,
    date_start=st.session_state.date_start,
    date_end=st.session_state.date_end,
    categories=st.session_state.selected_categories or _all_categories,
    regions=st.session_state.selected_regions or _all_regions,
)


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
# Empty-state guard  (T055)
# ---------------------------------------------------------------------------
if _filtered_df.empty:
    st.info("No data for selected filters.")
    st.stop()


# ---------------------------------------------------------------------------
# Sales trend chart  (US2)
# ---------------------------------------------------------------------------
st.subheader("Sales Trend")
# Using st.plotly_chart: build_trend_chart() returns a Plotly Figure because
# st.line_chart does not support custom y-axis labels ("Sales ($)") natively.
# T050: granularity reads/writes session_state for consistency across re-renders.
st.session_state.granularity = st.radio(
    "Granularity",
    ["Monthly", "Daily"],
    index=["Monthly", "Daily"].index(st.session_state.granularity),
    horizontal=True,
)
_trend_df = data.aggregate_by_time(_filtered_df, st.session_state.granularity)
st.plotly_chart(charts.build_trend_chart(_trend_df), use_container_width=True)


# ---------------------------------------------------------------------------
# Category and region bar charts  (US3)
# ---------------------------------------------------------------------------
# Using st.plotly_chart: build_bar_chart() returns Plotly Figures because
# st.bar_chart sorts bars alphabetically, losing the descending-by-value order.
st.subheader("Sales by Segment")
_col_cat, _col_reg = st.columns(2)
with _col_cat:
    _cat_df = data.aggregate_by_column(_filtered_df, "category")
    st.plotly_chart(
        charts.build_bar_chart(_cat_df, "label", "total_sales", "Sales by Category"),
        use_container_width=True,
    )
with _col_reg:
    _reg_df = data.aggregate_by_column(_filtered_df, "region")
    st.plotly_chart(
        charts.build_bar_chart(_reg_df, "label", "total_sales", "Sales by Region"),
        use_container_width=True,
    )
