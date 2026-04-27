import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.db_connect import get_engine

engine = get_engine()

# Load data
df = pd.read_sql("""
SELECT sale_date, quantity, price
FROM sales s JOIN products p ON s.product_id=p.product_id
""", engine)

# Feature Engineering
df['month'] = pd.to_datetime(df['sale_date']).dt.month
df['revenue'] = df['quantity'] * df['price']

X = df[['month']]
y = df['revenue']

# Train model
model = LinearRegression()
model.fit(X, y)

model_path = Path(__file__).resolve().with_name("revenue_model.pkl")
joblib.dump(model, model_path)
print("MODEL TRAINED & SAVED ✅")
