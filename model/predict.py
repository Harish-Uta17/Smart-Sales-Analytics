import joblib
from pathlib import Path

model_path = Path(__file__).resolve().with_name("revenue_model.pkl")
model = joblib.load(model_path)

month = int(input("Enter month number (1-12): "))
prediction = model.predict([[month]])

print("Predicted Revenue:", round(prediction[0],2))
