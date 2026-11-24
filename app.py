
import streamlit as st
import pandas as pd
import plotly.express as px

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

@st.cache_data
def load_data():

    inventory = pd.read_csv("data/cleaned/inventory_clean.csv")
    sales = pd.read_csv("data/cleaned/sales_clean.csv")
    products = pd.read_csv("data/cleaned/products_clean.csv")
    optimization = pd.read_csv("data/cleaned/inventory_optimization.csv")
    abc = pd.read_csv("data/cleaned/abc_classification.csv")

    return inventory, sales, products, optimization, abc


inventory, sales, products, optimization, abc = load_data()

# --------------------------------
# DASHBOARD HEADER
# --------------------------------

st.title("📦 Supply Chain & Inventory Optimization")

st.caption(
    "Inventory monitoring, replenishment planning "
    "and supply chain performance analytics"
)

st.divider()

# --------------------------------
# SIDEBAR FILTER
# --------------------------------

st.sidebar.header("Dashboard Filters")

selected_products = st.sidebar.multiselect(
    "Select Products",
    options=inventory["product_id"].dropna().unique(),
    default=inventory["product_id"].dropna().unique()
)

filtered_inventory = inventory[
    inventory["product_id"].isin(selected_products)
]

filtered_optimization = optimization[
    optimization["product_id"].isin(selected_products)
]

filtered_abc = abc[
    abc["product_id"].isin(selected_products)
]

filtered_sales = sales[
    sales["product_id"].isin(selected_products)
]

# --------------------------------
# KPI CALCULATIONS
# --------------------------------

total_products = filtered_inventory["product_id"].nunique()

total_stock = filtered_inventory["stock_quantity"].sum()

reorder_count = (
    filtered_optimization["replenishment_status"]
    == "Reorder Required"
).sum()

average_lead_time = filtered_optimization["lead_time_days"].mean()

total_inventory_value = filtered_abc["inventory_value"].sum()

# --------------------------------
# KPI CARDS
# --------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Products",
    f"{total_products:,}"
)

col2.metric(
    "Total Stock Units",
    f"{total_stock:,.0f}"
)

col3.metric(
    "Products to Reorder",
    f"{reorder_count:,}"
)

col4.metric(
    "Avg. Lead Time",
    f"{average_lead_time:.1f} days"
)

col5.metric(
    "Inventory Value",
    f"{total_inventory_value:,.0f}"
)

st.divider()

# --------------------------------
# INVENTORY LEVELS
# --------------------------------

st.subheader("Inventory Levels by Product")

inventory_chart = (
    filtered_inventory.groupby("product_id")["stock_quantity"]
    .sum()
    .reset_index()
)

fig_inventory = px.bar(
    inventory_chart,
    x="product_id",
    y="stock_quantity",
    title="Current Inventory Levels",
    color="stock_quantity"
)

st.plotly_chart(fig_inventory, use_container_width=True)

# --------------------------------
# REPLENISHMENT ANALYSIS
# --------------------------------

st.subheader("Replenishment Analysis")

col1, col2 = st.columns(2)

with col1:

    status_counts = (
        filtered_optimization["replenishment_status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = ["Status", "Count"]

    fig_status = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Replenishment Status Distribution",
        hole=0.4
    )

    st.plotly_chart(fig_status, use_container_width=True)

with col2:

    supplier_data = (
        filtered_optimization
        .groupby("product_id")["lead_time_days"]
        .mean()
        .reset_index()
    )

    fig_lead = px.bar(
        supplier_data,
        x="product_id",
        y="lead_time_days",
        title="Product Lead Time Analysis"
    )

    st.plotly_chart(fig_lead, use_container_width=True)

# --------------------------------
# ABC CLASSIFICATION
# --------------------------------

st.subheader("ABC Inventory Classification")

abc_counts = (
    filtered_abc["abc_category"]
    .value_counts()
    .reset_index()
)

abc_counts.columns = ["Category", "Products"]

fig_abc = px.pie(
    abc_counts,
    names="Category",
    values="Products",
    title="ABC Classification Distribution"
)

st.plotly_chart(fig_abc, use_container_width=True)

# --------------------------------
# DAILY SALES TREND
# --------------------------------

st.subheader("Sales Performance")

filtered_sales["date"] = pd.to_datetime(filtered_sales["date"])

daily_sales = (
    filtered_sales.groupby("date")["units_sold"]
    .sum()
    .reset_index()
)

fig_sales = px.line(
    daily_sales,
    x="date",
    y="units_sold",
    title="Daily Sales Trend",
    markers=True
)

st.plotly_chart(fig_sales, use_container_width=True)

# --------------------------------
# REORDER TABLE
# --------------------------------

st.subheader("Products Requiring Replenishment")

reorder_products = filtered_optimization[
    filtered_optimization["replenishment_status"]
    == "Reorder Required"
]

st.dataframe(
    reorder_products,
    use_container_width=True,
    hide_index=True
)

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "Supply Chain & Inventory Optimization Dashboard | "
    "Python | Pandas | Streamlit | Plotly"
)
