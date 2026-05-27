import os
from pathlib import Path
from typing import Optional

import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from scripts.demo_data import build_demo_dataset


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_URL = "mysql+pymysql://root:password@localhost:3306/demo"
DEFAULT_SQLITE_PATH = ROOT / "data" / "demo.sqlite"


def _demo_customers() -> pd.DataFrame:
    customers, _, _ = build_demo_dataset()
    return customers


def _demo_products() -> pd.DataFrame:
    _, products, _ = build_demo_dataset()
    return products


def _demo_sales() -> pd.DataFrame:
    _, _, sales = build_demo_dataset()
    return sales


def _seed_demo_sqlite(engine: Engine) -> None:
    customers = _demo_customers()
    products = _demo_products()
    sales = _demo_sales()

    with engine.begin() as conn:
        customers.to_sql("customers", conn, if_exists="replace", index=False)
        products.to_sql("products", conn, if_exists="replace", index=False)
        sales.to_sql("sales", conn, if_exists="replace", index=False)


def _create_sqlite_fallback_engine() -> Engine:
    DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite+pysqlite:///{DEFAULT_SQLITE_PATH.as_posix()}", pool_pre_ping=True)
    _seed_demo_sqlite(engine)
    return engine


def get_database_url() -> str:
    """Resolve DB URL from environment first, then Streamlit secrets, then local default."""
    env_url = os.getenv("DB_URL")
    if env_url:
        return env_url

    # Optional Streamlit secrets fallback when running the dashboard.
    try:
        import streamlit as st  # type: ignore

        secret_url: Optional[str] = st.secrets.get("DB_URL")
        if secret_url:
            return secret_url
    except Exception:
        pass

    return DEFAULT_DB_URL


def get_database_url_sources() -> dict[str, Optional[str]]:
    """Return discovered DB URL sources in resolution order."""
    env_url = os.getenv("DB_URL")
    secret_url: Optional[str] = None
    try:
        import streamlit as st  # type: ignore

        secret_url = st.secrets.get("DB_URL")
    except Exception:
        pass

    return {
        "env": env_url,
        "streamlit_secrets": secret_url,
        "default_local": DEFAULT_DB_URL,
    }


def get_engine() -> Engine:
    """Create and validate an engine from env, secrets, or local fallback."""
    sources = get_database_url_sources()

    candidates: list[tuple[str, str]] = []
    if sources["env"]:
        candidates.append(("env:DB_URL", sources["env"]))
    if sources["streamlit_secrets"]:
        candidates.append(("streamlit:secrets.DB_URL", sources["streamlit_secrets"]))
    candidates.append(("default_local", sources["default_local"]))

    # Remove duplicate URLs while preserving priority order.
    deduped: list[tuple[str, str]] = []
    seen: set[str] = set()
    for source_name, url in candidates:
        if url and url not in seen:
            deduped.append((source_name, url))
            seen.add(url)

    failures: list[str] = []

    for source_name, db_url in deduped:
        connect_args = {}
        if "supabase.com" in db_url and "sslmode=" not in db_url:
            connect_args = {"sslmode": "require"}

        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args=connect_args,
        )

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine
        except Exception as exc:
            failures.append(f"{source_name} -> {exc}")

    return _create_sqlite_fallback_engine()


def check_connection(engine: Optional[Engine] = None) -> None:
    """Raise an exception if database connection is invalid."""
    engine = engine or get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


if __name__ == "__main__":
    try:
        check_connection()
        print("CONNECTED SUCCESSFULLY")
    except Exception as exc:
        print("CONNECTION FAILED")
        print(exc)
