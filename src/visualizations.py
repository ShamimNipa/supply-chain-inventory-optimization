
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Create output directory
os.makedirs("reports/figures", exist_ok=True)

# Load datasets
inventory = pd.read_csv("data/cleaned/inventory_clean.csv")
sales = pd.read_csv("data/cleaned/sales_clean.csv")
products = pd.read_csv("data/cleaned/products_clean.csv")

# Visualization style
sns.set_theme(style="whitegrid")


# ==========================================
# 1. INVENTORY LEVELS BY PRODUCT
# ==========================================

inventory_summary = (
    inventory.groupby("product_id")["stock_quantity"]
    .sum()
    .reset_index()
)

inventory_summary = inventory_summary.merge(
    products[["product_id", "product_name"]],
    on="product_id",
    how="left"
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=inventory_summary,
    x="product_name",
    y="stock_quantity"
)

plt.title("Inventory Levels by Product")
plt.xlabel("Product")
plt.ylabel("Total Stock Quantity")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("reports/figures/inventory_levels.png")
plt.close()


# ==========================================
# 2. REPLENISHMENT STATUS
# ==========================================

replenishment = inventory.merge(
    products[["product_id", "reorder_threshold"]],
    on="product_id",
    how="left"
)

replenishment["status"] = np.where(
    replenishment["stock_quantity"] <= replenishment["reorder_threshold"],
    "Reorder Required",
    "Sufficient Stock"
)

plt.figure(figsize=(8, 5))

sns.countplot(
    data=replenishment,
    x="status"
)

plt.title("Inventory Replenishment Status")
plt.xlabel("Replenishment Status")
plt.ylabel("Number of Warehouse-Product Records")
plt.tight_layout()

plt.savefig("reports/figures/replenishment_status.png")
plt.close()


# ==========================================
# 3. SUPPLIER INVENTORY VALUE
# ==========================================

supplier_data = inventory.merge(
    products[["product_id", "supplier_id", "unit_cost"]],
    on="product_id",
    how="left"
)

supplier_data["inventory_value"] = (
    supplier_data["stock_quantity"] *
    supplier_data["unit_cost"]
)

supplier_summary = (
    supplier_data.groupby("supplier_id")["inventory_value"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=supplier_summary,
    x="supplier_id",
    y="inventory_value"
)

plt.title("Inventory Value by Supplier")
plt.xlabel("Supplier ID")
plt.ylabel("Inventory Value")
plt.tight_layout()

plt.savefig("reports/figures/supplier_inventory_value.png")
plt.close()


# ==========================================
# 4. ABC INVENTORY CLASSIFICATION
# ==========================================

abc = inventory.merge(
    products[["product_id", "product_name", "unit_cost"]],
    on="product_id",
    how="left"
)

abc["inventory_value"] = (
    abc["stock_quantity"] * abc["unit_cost"]
)

abc = (
    abc.groupby(["product_id", "product_name"])["inventory_value"]
    .sum()
    .reset_index()
)

abc = abc.sort_values(
    by="inventory_value",
    ascending=False
)

total_value = abc["inventory_value"].sum()

abc["cumulative_percentage"] = (
    abc["inventory_value"].cumsum() / total_value * 100
)

abc["abc_category"] = np.select(
    [
        abc["cumulative_percentage"] <= 80,
        abc["cumulative_percentage"] <= 95
    ],
    ["A", "B"],
    default="C"
)

plt.figure(figsize=(8, 5))

sns.countplot(
    data=abc,
    x="abc_category",
    order=["A", "B", "C"]
)

plt.title("ABC Inventory Classification")
plt.xlabel("ABC Category")
plt.ylabel("Number of Products")
plt.tight_layout()

plt.savefig("reports/figures/abc_classification.png")
plt.close()


# ==========================================
# 5. DAILY SALES TREND
# ==========================================

sales["date"] = pd.to_datetime(sales["date"])

daily_sales = (
    sales.groupby("date")["units_sold"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=daily_sales,
    x="date",
    y="units_sold"
)

plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("reports/figures/daily_sales_trend.png")
plt.close()


# ==========================================
# SAVE ANALYTICAL DATASETS
# ==========================================

replenishment.to_csv(
    "data/cleaned/replenishment_analysis.csv",
    index=False
)

abc.to_csv(
    "data/cleaned/abc_classification.csv",
    index=False
)

supplier_summary.to_csv(
    "data/cleaned/supplier_analysis.csv",
    index=False
)


print("\n================================")
print("VISUALIZATION COMPLETED!")
print("================================")

print("\nReplenishment Summary:")
print(replenishment["status"].value_counts())

print("\nABC Classification:")
print(abc["abc_category"].value_counts())

print("\nSupplier Inventory Value:")
print(supplier_summary)

print("\nAll charts saved in reports/figures/")

