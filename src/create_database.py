import pandas as pd
import sqlite3
from pathlib import Path

# Find project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
DB_PATH = BASE_DIR / "data" / "supply_chain.db"

# Load cleaned CSV files
products = pd.read_csv(DATA_DIR / "products_clean.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers_clean.csv")
inventory = pd.read_csv(DATA_DIR / "inventory_clean.csv")
sales = pd.read_csv(DATA_DIR / "sales_clean.csv")

# Create SQLite database
connection = sqlite3.connect(DB_PATH)

# Insert datasets as database tables
products.to_sql("products", connection, if_exists="replace", index=False)

suppliers.to_sql("suppliers", connection, if_exists="replace", index=False)

inventory.to_sql("inventory", connection, if_exists="replace", index=False)

sales.to_sql("sales", connection, if_exists="replace", index=False)

# Create indexes to help with common queries
connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id)"
)

connection.execute(
    "CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id)"
)

connection.commit()
connection.close()

print("SQLite database created successfully!")
print(f"Database location: {DB_PATH}")