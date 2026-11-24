
import pandas as pd
import numpy as np
from pathlib import Path

# Make results reproducible
np.random.seed(42)

# Project data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# --------------------------------
# 1. PRODUCTS DATA
# --------------------------------

products = pd.DataFrame({
    "product_id": range(1, 21),

    "product_name": [
        "Laptop", "Mouse", "Keyboard", "Monitor",
        "Headphones", "Printer", "Webcam", "Router",
        "Smartphone", "Tablet", "USB Drive", "SSD",
        "RAM", "Power Bank", "Speaker", "Microphone",
        "Smart Watch", "Charger", "Graphics Card", "Hard Drive"
    ],

    "category": [
        "Electronics", "Accessories", "Accessories", "Electronics",
        "Accessories", "Electronics", "Accessories", "Electronics",
        "Electronics", "Electronics", "Storage", "Storage",
        "Components", "Accessories", "Accessories", "Accessories",
        "Electronics", "Accessories", "Components", "Storage"
    ],

    "unit_cost": np.random.randint(10, 800, 20),

    "supplier_id": np.random.randint(1, 6, 20),

    "reorder_threshold": np.random.randint(20, 100, 20)
})

products["selling_price"] = (
    products["unit_cost"] * 1.3
).round(2)

# --------------------------------
# 2. SUPPLIERS DATA
# --------------------------------

suppliers = pd.DataFrame({
    "supplier_id": range(1, 6),

    "supplier_name": [
        "Global Tech Supplies",
        "Asia Electronics Ltd",
        "Digital Parts Co",
        "Prime Components",
        "Smart Supply Group"
    ],

    "region": [
        "Asia", "Europe", "Asia", "North America", "Asia"
    ],

    "expected_lead_time_days": [7, 12, 9, 15, 6]
})

# --------------------------------
# 3. INVENTORY DATA
# --------------------------------

warehouses = ["Dhaka", "Chattogram", "Sylhet"]

inventory_records = []

for _, product in products.iterrows():

    for warehouse in warehouses:

        inventory_records.append({
            "product_id": product["product_id"],
            "warehouse": warehouse,
            "stock_quantity": np.random.randint(5, 250),
            "safety_stock": np.random.randint(10, 40)
        })

inventory = pd.DataFrame(inventory_records)

# --------------------------------
# 4. SALES DATA
# --------------------------------

dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    freq="D"
)

sales_records = []

for date in dates:

    for product_id in products["product_id"]:

        sales_records.append({
            "date": date,
            "product_id": product_id,
            "warehouse": np.random.choice(warehouses),
            "units_sold": np.random.poisson(lam=5)
        })

sales = pd.DataFrame(sales_records)

# --------------------------------
# 5. SAVE CSV FILES
# --------------------------------

products.to_csv(DATA_DIR / "products.csv", index=False)

suppliers.to_csv(DATA_DIR / "suppliers.csv", index=False)

inventory.to_csv(DATA_DIR / "inventory.csv", index=False)

sales.to_csv(DATA_DIR / "sales.csv", index=False)

print("Dataset generation completed!")

print("\nDataset sizes:")
print("Products:", len(products))
print("Suppliers:", len(suppliers))
print("Inventory:", len(inventory))
print("Sales:", len(sales))

print(f"\nCSV files saved in: {DATA_DIR}")
