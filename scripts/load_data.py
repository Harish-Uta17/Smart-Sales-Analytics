import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.db_connect import get_engine
from scripts.demo_data import build_demo_dataset

engine = get_engine()

customers, products, sales = build_demo_dataset(n_customers=120, n_sales=10000)

with engine.begin() as conn:
    conn.exec_driver_sql("DROP TABLE IF EXISTS sales")
    conn.exec_driver_sql("DROP TABLE IF EXISTS products")
    conn.exec_driver_sql("DROP TABLE IF EXISTS customers")

customers.to_sql("customers", engine, if_exists="append", index=False)
products.to_sql("products", engine, if_exists="append", index=False)
sales.to_sql("sales", engine, if_exists="append", index=False)

print(f"DATA INSERTED SUCCESSFULLY ({len(customers)} customers, {len(products)} products, {len(sales)} sales rows)")
