import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.db_connect import get_engine

engine = get_engine()
replace_mode = engine.dialect.name == "sqlite"

customers = pd.DataFrame({
    "customer_id":[1,2,3],
    "name":["Rahul","Anita","Suresh"],
    "city":["Bangalore","Hyderabad","Chennai"],
    "age":[22,24,27]
})

products = pd.DataFrame({
    "product_id":[101,102,103,104,105,106,107,108,109,110],
    "product_name":["Laptop","Mobile","Headphones","Smartwatch","Tablet","Keyboard","Mouse","Monitor","Speaker","Webcam"],
    "categoty":["Electronics","Electronics","Accessories","Wearables","Electronics","Accessories","Accessories","Electronics","Accessories","Accessories"],
    "price":[50000,30000,3000,12000,25000,2500,1500,18000,4500,6000]
})

sales = pd.DataFrame({
    "customer_id":[1,2,3,1,2,3,1,2,3,1,2,3,1,2,3],
    "product_id":[101,102,103,104,105,106,107,108,109,110,102,105,108,109,103],
    "quantity":[1,2,3,1,1,4,2,1,3,2,1,2,1,2,4],
    "sale_date":["2024-01-10","2024-01-12","2024-02-05","2024-02-14","2024-02-20","2024-02-28","2024-03-01","2024-03-08","2024-03-15","2024-03-22","2024-04-02","2024-04-10","2024-04-18","2024-05-03","2024-05-15"]
})

write_mode = "replace" if replace_mode else "append"

customers.to_sql("customers", engine, if_exists=write_mode, index=False)
products.to_sql("products", engine, if_exists=write_mode, index=False)
sales.to_sql("sales", engine, if_exists=write_mode, index=False)

print("DATA INSERTED SUCCESSFULLY")
