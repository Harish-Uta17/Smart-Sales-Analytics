import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.db_connect import get_engine

engine = get_engine()

query = """
SELECT 
    p.categoty,
    SUM(s.quantity * p.price) AS total_revenue,
    COUNT(DISTINCT s.customer_id) AS unique_customers
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.categoty;
"""

kpis = pd.read_sql(query, engine)
print("\n=== BUSINESS KPIs ===\n")
print(kpis)
