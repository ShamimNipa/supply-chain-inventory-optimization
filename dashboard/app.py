
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data" / "cleaned"

@st.cache_data
def load_data():

    inventory = pd.read_csv(
        DATA_DIR / "inventory_clean.csv"
    )

    optimization = pd.read_csv(
        REPORT_DIR / "inventory_optimization_results.csv"
    )

    abc = pd.read_csv(
        REPORT_DIR / "abc_inventory_analysis.csv"
    )

    supplier = pd.read_csv(
        REPORT_DIR / "supplier_performance.csv"
    )

    return inventory, optimization, abc, supplier


inventory, optimization, abc, supplier = load_data()

# --------------------------------
# DASHBOARD TITLE
# --------------------------------

st.title("📦 Supply Chain & Inventory Optimization")

st.caption(
    "Inventory monitoring, demand analysis, "
    "replenishment planning and supplier performance."
)

st.divider()

# --------------------------------
# SIDEBAR FILTER
# --------------------------------

st.sidebar.header("Dashboard Filters")

categories = ["All"] + sorted(
    optimization["category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Product Category",
    categories
)

filtered = optimization.copy()

if selected_category != "All":
    filtered = filtered[
        filtered["category"] == selected_category
    ]

# --------------------------------
# KPI CARDS
# --------------------------------

total_products = len(filtered)

total_stock = filtered["current_stock"].sum()

total_inventory_value = (
    filtered["current_stock"] * filtered["unit_cost"]
).sum()

reorder_count = (
    filtered["reorder_status"] == "Reorder Required"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Products",
    f"{total_products:,}"
)

col2.metric(
    "Total Stock Units",
    f"{total_stock:,.0f}"
)

col3.metric(
    "Inventory Value",
    f"{total_inventory_value:,.2f}"
)

col4.metric(
    "Products to Reorder",
    f"{reorder_count:,}"
)

st.divider()

# --------------------------------
# INVENTORY STATUS
# --------------------------------

st.subheader("Inventory Status")

status_counts = (
    filtered["reorder_status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = ["Status", "Products"]

fig_status = px.pie(
    status_counts,
    names="Status",
    values="Products",
    hole=0.45,
    title="Reorder Status Distribution"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)

# --------------------------------
# ABC ANALYSIS
# --------------------------------

st.subheader("ABC Inventory Classification")

abc_filtered = filtered[
    ["product_id", "product_name", "abc_category"]
]

abc_counts = (
    abc_filtered["abc_category"]
    .value_counts()
    .reset_index()
)

abc_counts.columns = ["ABC Category", "Products"]

fig_abc = px.bar(
    abc_counts,
    x="ABC Category",
    y="Products",
    title="Products by ABC Category",
    text="Products"
)

st.plotly_chart(
    fig_abc,
    use_container_width=True
)

# --------------------------------
# STOCK VS REORDER POINT
# --------------------------------

st.subheader("Current Stock vs Reorder Point")

stock_chart = px.bar(
    filtered,
    x="product_name",
    y=["current_stock", "reorder_point"],
    barmode="group",
    title="Product Stock Comparison"
)

stock_chart.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="Product",
    yaxis_title="Units"
)

st.plotly_chart(
    stock_chart,
    use_container_width=True
)

# --------------------------------
# SUPPLIER PERFORMANCE
# --------------------------------

st.subheader("Supplier Performance")

if not supplier.empty:

    supplier_chart = px.bar(
        supplier,
        x="supplier_id",
        y="on_time_rate",
        title="Supplier On-Time Delivery Rate",
        labels={
            "supplier_id": "Supplier ID",
            "on_time_rate": "On-Time Delivery (%)"
        },
        text="on_time_rate"
    )

    st.plotly_chart(
        supplier_chart,
        use_container_width=True
    )

# --------------------------------
# REPLENISHMENT TABLE
# --------------------------------

st.subheader("Replenishment Recommendations")

st.dataframe(
    filtered[
        [
            "product_name",
            "abc_category",
            "current_stock",
            "reorder_point",
            "suggested_order_quantity",
            "reorder_status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------
# DOWNLOAD REPORT
# --------------------------------

st.subheader("Download Analysis")

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Inventory Optimization Report",
    data=csv_data,
    file_name="inventory_optimization_report.csv",
    mime="text/csv"
)

st.caption(
    "Note: This dashboard uses simulated data "
    "for analytical demonstration."
)
