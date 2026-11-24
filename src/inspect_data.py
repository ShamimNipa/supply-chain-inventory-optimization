
import pandas as pd

files = {
    "INVENTORY": "data/cleaned/inventory_clean.csv",
    "SALES": "data/cleaned/sales_clean.csv",
    "PRODUCTS": "data/cleaned/products_clean.csv",
}

for name, path in files.items():
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    df = pd.read_csv(path)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    print("\nDataset shape:")
    print(df.shape)
