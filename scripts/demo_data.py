from __future__ import annotations

import numpy as np
import pandas as pd


def generate_customers(n_customers: int = 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    first_names = np.array(
        [
            "Rahul",
            "Anita",
            "Suresh",
            "Priya",
            "Aman",
            "Neha",
            "Vikram",
            "Pooja",
            "Arjun",
            "Meera",
            "Karan",
            "Isha",
        ]
    )
    last_names = np.array(
        [
            "Sharma",
            "Verma",
            "Iyer",
            "Patel",
            "Singh",
            "Reddy",
            "Nair",
            "Gupta",
            "Mehta",
            "Kumar",
            "Bose",
            "Joshi",
        ]
    )
    cities = np.array(
        [
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Mumbai",
            "Delhi",
            "Pune",
            "Kolkata",
            "Ahmedabad",
        ]
    )
    city_weights = np.array([0.18, 0.16, 0.14, 0.16, 0.12, 0.10, 0.10, 0.04])

    customer_ids = np.arange(1, n_customers + 1)
    names = [
        f"{rng.choice(first_names)} {rng.choice(last_names)} {idx:03d}"
        for idx in customer_ids
    ]

    return pd.DataFrame(
        {
            "customer_id": customer_ids,
            "name": names,
            "city": rng.choice(cities, size=n_customers, p=city_weights),
            "age": rng.integers(21, 61, size=n_customers),
        }
    )


def generate_products() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],
            "product_name": [
                "Laptop",
                "Mobile",
                "Headphones",
                "Smartwatch",
                "Tablet",
                "Keyboard",
                "Mouse",
                "Monitor",
                "Speaker",
                "Webcam",
                "Router",
                "Printer",
            ],
            "categoty": [
                "Electronics",
                "Electronics",
                "Accessories",
                "Wearables",
                "Electronics",
                "Accessories",
                "Accessories",
                "Electronics",
                "Accessories",
                "Accessories",
                "Electronics",
                "Electronics",
            ],
            "price": [50000, 30000, 3000, 12000, 25000, 2500, 1500, 18000, 4500, 6000, 8500, 14000],
        }
    )


def generate_sales(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    n_rows: int = 10000,
    start_date: str = "2023-01-01",
    end_date: str = "2025-05-31",
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    total_days = max((end - start).days, 1)

    customer_ids = customers["customer_id"].to_numpy()
    product_ids = products["product_id"].to_numpy()
    product_weights = products["price"].to_numpy(dtype=float)
    product_weights = product_weights / product_weights.sum()

    offsets = rng.integers(0, total_days + 1, size=n_rows)
    sale_dates = start + pd.to_timedelta(offsets, unit="D")
    time_factor = offsets / max(total_days, 1)
    seasonal_boost = 1 + 0.35 * np.sin(2 * np.pi * (sale_dates.month.to_numpy() / 12.0))

    base_quantity = rng.integers(1, 4, size=n_rows)
    trend_quantity = np.floor(time_factor * 3).astype(int)
    quantity = np.clip(base_quantity + trend_quantity + (seasonal_boost > 1.1).astype(int), 1, 8)

    return pd.DataFrame(
        {
            "customer_id": rng.choice(customer_ids, size=n_rows),
            "product_id": rng.choice(product_ids, size=n_rows, p=product_weights),
            "quantity": quantity,
            "sale_date": sale_dates.strftime("%Y-%m-%d"),
        }
    )


def build_demo_dataset(
    n_customers: int = 120,
    n_sales: int = 10000,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = generate_customers(n_customers=n_customers, seed=seed)
    products = generate_products()
    sales = generate_sales(customers, products, n_rows=n_sales, seed=seed)
    return customers, products, sales