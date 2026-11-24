
import pandas as pd
import numpy as np
import os

# --------------------------------
# 1. Load datasets
# --------------------------------

inventory = pd.read_csv("data/cleaned/inventory_clean.csv")
sales = pd.read_csv("data/cleaned/sales_clean.csv")
products = pd.read_csv("data/cleaned/products_clean.csv")
purchase_orders = pd.read_csv("data/cleaned/purchase_orders.csv")

os.makedirs("data/cleaned", exist_ok=True)

# --------------------------------
# 2. Calculate Average Daily Demand
# --------------------------------

sales["date"] = pd.to_datetime(sales["date"])

total_days = (
    sales["date"].max() - sales["date"].min()
).days + 1

daily_demand = (
    sales.groupby(["product_id", "warehouse"])["units_sold"]
    .sum()
    .reset_index()
)

daily_demand["average_daily_demand"] = (
    daily_demand["units_sold"] / total_days
)

# --------------------------------
# 3. Calculate Supplier Lead Time
# --------------------------------

purchase_orders["order_date"] = pd.to_datetime(
    purchase_orders["order_date"]
)

purchase_orders["actual_delivery_date"] = pd.to_datetime(
    purchase_orders["actual_delivery_date"]
)

purchase_orders["lead_time_days"] = (
    purchase_orders["actual_delivery_date"]
    - purchase_orders["order_date"]
).dt.days

supplier_lead_time = (
    purchase_orders.groupby("product_id")["lead_time_days"]
    .mean()
    .reset_index()
)

# --------------------------------
# 4. Merge datasets
# --------------------------------

optimization = inventory.merge(
    daily_demand[
        ["product_id", "warehouse", "average_daily_demand"]
    ],
    on=["product_id", "warehouse"],
    how="left"
)

optimization = optimization.merge(
    supplier_lead_time,
    on="product_id",
    how="left"
)

optimization = optimization.merge(
    products[
        ["product_id", "product_name", "reorder_threshold"]
    ],
    on="product_id",
    how="left"
)

optimization["average_daily_demand"] = (
    optimization["average_daily_demand"].fillna(0)
)

optimization["lead_time_days"] = (
    optimization["lead_time_days"].fillna(0)
)

# --------------------------------
# 5. Calculate Reorder Point
# --------------------------------

optimization["reorder_point"] = (
    optimization["average_daily_demand"]
    * optimization["lead_time_days"]
    + optimization["safety_stock"]
)

# --------------------------------
# 6. Replenishment Status
# --------------------------------

optimization["replenishment_status"] = np.where(
    optimization["stock_quantity"]
    <= optimization["reorder_point"],
    "Reorder Required",
    "Sufficient Stock"
)

# --------------------------------
# 7. ABC Classification
# --------------------------------

products["inventory_value"] = (
    products["unit_cost"]
    * products["reorder_threshold"]
)

products = products.sort_values(
    by="inventory_value",
    ascending=False
)

total_value = products["inventory_value"].sum()

if total_value > 0:
    products["cumulative_percentage"] = (
        products["inventory_value"].cumsum()
        / total_value
    )

    products["abc_category"] = pd.cut(
        products["cumulative_percentage"],
        bins=[0, 0.80, 0.95, 1.01],
        labels=["A", "B", "C"],
        include_lowest=True
    )
else:
    products["cumulative_percentage"] = 0
    products["abc_category"] = "C"

# --------------------------------
# 8. Save results
# --------------------------------

optimization.to_csv(
    "data/cleaned/inventory_optimization.csv",
    index=False
)

products.to_csv(
    "data/cleaned/abc_classification.csv",
    index=False
)

# --------------------------------
# 9. Display results
# --------------------------------

print("\nInventory Optimization Completed!")

print("\nReplenishment Status:")
print(
    optimization["replenishment_status"].value_counts()
)

print("\nABC Classification:")
print(
    products["abc_category"].value_counts()
)

print("\nAverage Supplier Lead Time:")
print(
    round(purchase_orders["lead_time_days"].mean(), 2),
    "days"
)

print("\nGenerated Files:")
print("- inventory_optimization.csv")
print("- abc_classification.csv")
