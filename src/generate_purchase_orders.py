
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "cleaned"

products = pd.read_csv(DATA_DIR / "products_clean.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers_clean.csv")

warehouses = ["Dhaka", "Chattogram", "Sylhet"]

records = []

# Generate 300 purchase orders
for order_id in range(1, 301):

    product = products.sample(1).iloc[0]

    supplier = suppliers[
        suppliers["supplier_id"] == product["supplier_id"]
    ].iloc[0]

    order_date = pd.Timestamp("2025-01-01") + pd.Timedelta(
        days=int(np.random.randint(0, 330))
    )

    expected_lead_time = int(
        supplier["expected_lead_time_days"]
    )

    # Simulate actual delivery variation
    delay = int(np.random.choice(
        [-3, -2, -1, 0, 1, 2, 3, 5, 7, 10],
        p=[0.05, 0.05, 0.10, 0.25, 0.15,
           0.12, 0.10, 0.08, 0.06, 0.04]
    ))

    actual_lead_time = max(1, expected_lead_time + delay)

    expected_delivery_date = (
        order_date + pd.Timedelta(days=expected_lead_time)
    )

    actual_delivery_date = (
        order_date + pd.Timedelta(days=actual_lead_time)
    )

    records.append({
        "order_id": order_id,
        "supplier_id": int(supplier["supplier_id"]),
        "product_id": int(product["product_id"]),
        "warehouse": np.random.choice(warehouses),
        "order_date": order_date,
        "expected_delivery_date": expected_delivery_date,
        "actual_delivery_date": actual_delivery_date,
        "quantity_ordered": int(np.random.randint(20, 200))
    })

purchase_orders = pd.DataFrame(records)

purchase_orders.to_csv(
    DATA_DIR / "purchase_orders.csv",
    index=False
)

print("Purchase orders generated successfully!")
print("Total purchase orders:", len(purchase_orders))
