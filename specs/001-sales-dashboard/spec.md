# Feature Specification: ShopSmart Sales Analytics Dashboard

**Feature Branch**: `001-sales-dashboard`
**Created**: 2026-03-12
**Status**: Draft
**Input**: E-Commerce Analytics Dashboard — Streamlit sales data visualization with KPI
scorecards, trend chart, category and region bar charts (from prd/ecommerce-analytics.md)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View KPI Scorecards (Priority: P1)

A finance manager opens the dashboard and immediately sees four high-level metrics at the
top of the page: Total Sales, Total Orders, Average Order Value, and Top Category. No
interaction is required — the numbers are visible on load.

**Why this priority**: KPI scorecards are the first thing every stakeholder sees and the
core reason the dashboard exists. Without them, the dashboard has no MVP value.

**Independent Test**: Open the dashboard with the sample CSV loaded. Verify that four
metric cards are visible and that their values match manual calculations from the CSV
(Total Sales ≈ $650K–$700K, Total Orders = 482, AOV = Total Sales ÷ 482, Top Category =
highest-revenue category name).

**Acceptance Scenarios**:

1. **Given** the dashboard loads with `data/sales-data.csv`, **When** a user views the
   page, **Then** four KPI cards display: Total Sales (formatted as $X,XXX,XXX), Total
   Orders (integer), Average Order Value (formatted as $X,XXX), and Top Category (string).
2. **Given** the CSV contains valid data, **When** the dashboard renders, **Then** all
   four KPI values match the expected calculations from the raw data.
3. **Given** a date range filter is applied, **When** the filter changes, **Then** all
   four KPI cards update to reflect only the filtered data.

---

### User Story 2 - Explore Sales Trend Over Time (Priority: P2)

The CEO opens the dashboard and views a line chart showing sales revenue over time. They
can toggle between daily and monthly granularity using a control on the chart or sidebar
to zoom in or smooth out the trend.

**Why this priority**: The trend chart answers the most strategic question — is the
business growing? It is the primary analytical view after the top-level KPIs.

**Independent Test**: Open the dashboard. Verify a line chart is visible with time on the
x-axis and sales on the y-axis. Switch between daily and monthly granularity and confirm
the chart re-renders with the correct aggregation. Hover over a data point and verify the
tooltip shows the date and exact sales value.

**Acceptance Scenarios**:

1. **Given** the dashboard is loaded, **When** a user views the trend section, **Then** a
   line chart is displayed with labeled axes (time and sales amount).
2. **Given** the trend chart is visible, **When** a user selects "Monthly" granularity,
   **Then** the chart shows one data point per calendar month.
3. **Given** the trend chart is visible, **When** a user selects "Daily" granularity,
   **Then** the chart shows one data point per transaction date.
4. **Given** a date range filter is active, **When** the granularity is toggled, **Then**
   the chart respects both the date range and the selected granularity.

---

### User Story 3 - Analyse Sales by Category and Region (Priority: P3)

The marketing director and regional manager open the dashboard and view two bar charts
side by side: one showing sales by product category, the other by geographic region. Both
charts are sorted highest to lowest, making it easy to identify top and bottom performers.

**Why this priority**: Segment breakdowns are the primary analytical tool for the
marketing and regional management personas. They depend on the data pipeline established
in P1 and P2.

**Independent Test**: Open the dashboard. Verify two bar charts are visible. Confirm that
bars are sorted descending by sales value. Hover over a bar and verify the tooltip shows
the segment name and exact sales value. Apply a category filter and confirm the category
chart updates (and the region chart updates to reflect the filtered data).

**Acceptance Scenarios**:

1. **Given** the dashboard is loaded, **When** a user views the breakdown section, **Then**
   two bar charts are displayed: "Sales by Category" and "Sales by Region".
2. **Given** the bar charts are visible, **When** a user examines the order of bars,
   **Then** bars are sorted from highest to lowest sales value.
3. **Given** a category filter is applied, **When** a user views the region chart, **Then**
   the region data reflects only the selected categories.
4. **Given** a region filter is applied, **When** a user views the category chart, **Then**
   the category data reflects only the selected regions.

---

### User Story 4 - Filter Dashboard by Date, Category, and Region (Priority: P4)

Any stakeholder uses the sidebar filter controls to narrow the dashboard to a specific
time window, product category, or region. All charts and KPI cards update simultaneously
to reflect the filtered view.

**Why this priority**: Filtering enables self-service analysis for non-technical users,
directly addressing the PRD goal of eliminating manual report generation for specific
segments.

**Independent Test**: Apply a date range that covers only Q1 (January–March). Verify that
all four KPI cards, the trend chart, and both bar charts display only Q1 data. Then add a
category filter for "Electronics" and verify all views narrow further.

**Acceptance Scenarios**:

1. **Given** the sidebar is visible, **When** a user sets a start and end date, **Then**
   all charts and KPIs update to show only data within that range.
2. **Given** the sidebar is visible, **When** a user selects one or more categories from
   the multi-select, **Then** all views filter to show only those categories.
3. **Given** the sidebar is visible, **When** a user selects one or more regions from the
   multi-select, **Then** all views filter to show only those regions.
4. **Given** multiple filters are active, **When** any single filter changes, **Then** all
   views re-render immediately with the combined filter state.
5. **Given** filters are active, **When** a user clears all filters, **Then** all views
   return to showing the full dataset.

---

### Edge Cases

- What happens when the CSV file is missing or unreadable? The dashboard MUST display a
  clear error message rather than a blank page or Python traceback.
- What happens when a filter combination returns zero rows? All KPI cards show $0 / 0,
  and charts display an empty state with a "No data for selected filters" message.
- What happens if the CSV contains rows with null values in `total_amount`, `category`,
  or `region`? Those rows MUST be excluded from all aggregations, and the count of
  excluded rows MUST be surfaced as a warning in the UI.
- What happens when a user sets a date range where start > end? The dashboard MUST show a
  validation message and not render broken charts.
- What happens with very large date ranges (e.g., all-time)? The monthly view MUST remain
  legible; the daily view MAY show a warning if more than 365 data points are rendered.

## Requirements *(mandatory)*

### Functional Requirements

**KPI Scorecards**

- **FR-001**: The dashboard MUST display Total Sales as the sum of `total_amount` for all
  rows matching active filters, formatted as a US dollar currency string (e.g., $682,450).
- **FR-002**: The dashboard MUST display Total Orders as the count of unique `order_id`
  values matching active filters.
- **FR-003**: The dashboard MUST display Average Order Value as Total Sales ÷ Total Orders,
  formatted as a US dollar currency string.
- **FR-004**: The dashboard MUST display Top Category as the `category` value with the
  highest sum of `total_amount` among rows matching active filters.

**Sales Trend Chart**

- **FR-005**: The dashboard MUST display a line chart with time on the x-axis and total
  sales on the y-axis.
- **FR-006**: Users MUST be able to toggle between "Daily" and "Monthly" granularity for
  the trend chart; the default MUST be "Monthly".
- **FR-007**: The trend chart MUST display interactive tooltips showing the exact date/month
  label and sales value on hover.
- **FR-008**: The trend chart x-axis and y-axis MUST be labeled.

**Category and Region Bar Charts**

- **FR-009**: The dashboard MUST display a bar chart of total sales grouped by `category`,
  sorted descending by sales value.
- **FR-010**: The dashboard MUST display a bar chart of total sales grouped by `region`,
  sorted descending by sales value.
- **FR-011**: Both bar charts MUST display interactive tooltips showing the segment name
  and exact sales value on hover.
- **FR-012**: Both bar charts MUST have labeled axes.

**Filtering**

- **FR-013**: The dashboard MUST provide a date range picker (start date, end date) that
  filters all views to the selected range; default MUST be the full date range in the data.
- **FR-014**: The dashboard MUST provide a multi-select control for `category` that filters
  all views; default MUST be all categories selected.
- **FR-015**: The dashboard MUST provide a multi-select control for `region` that filters
  all views; default MUST be all regions selected.
- **FR-016**: All filter controls MUST be grouped together in a sidebar or filter panel.
- **FR-017**: All charts and KPI cards MUST re-render immediately when any filter changes.

**Data Loading**

- **FR-018**: The dashboard MUST load data from `data/sales-data.csv` by default.
- **FR-019**: If the CSV file is missing or cannot be parsed, the dashboard MUST display a
  user-friendly error message.
- **FR-020**: Rows with null values in `total_amount`, `category`, or `region` MUST be
  excluded from all aggregations; the count of excluded rows MUST be displayed as a
  UI warning.

**Branding**

- **FR-021**: The dashboard page title and header MUST read "ShopSmart Sales Dashboard".

### Key Entities

- **Transaction**: A single sales record; key attributes: `date`, `order_id`, `product`,
  `category`, `region`, `quantity`, `unit_price`, `total_amount`.
- **KPI**: A derived scalar metric computed from a filtered set of transactions (Total
  Sales, Total Orders, Average Order Value, Top Category).
- **Filter State**: The active combination of date range, selected categories, and selected
  regions that constrains which transactions are included in all views.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The dashboard fully loads and all charts are visible within 5 seconds on a
  standard broadband connection.
- **SC-002**: All four KPI card values match manual calculations from the raw CSV to within
  rounding of the displayed decimal places.
- **SC-003**: Switching between Daily and Monthly granularity on the trend chart takes no
  more than 2 seconds to re-render.
- **SC-004**: Applying any filter combination updates all charts and KPI cards within
  2 seconds.
- **SC-005**: A non-technical stakeholder can read and interpret all charts without any
  training or documentation (clear labels, titles, and tooltips on every visual element).
- **SC-006**: The dashboard runs without errors or console warnings when loaded with the
  provided `data/sales-data.csv`.
- **SC-007**: The dashboard is accessible via a public URL after deployment, with no
  installation required for end users.

## Assumptions

- The CSV schema matches exactly the structure defined in the PRD (`date`, `order_id`,
  `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`).
- All dates in the CSV are parseable as ISO 8601 (`YYYY-MM-DD`).
- "Total Orders" is the count of unique `order_id` values, not the count of rows.
- No authentication or access control is required for Phase 1 (public dashboard).
- The granularity toggle defaults to "Monthly" as it provides the cleanest view of
  the 12-month dataset.
