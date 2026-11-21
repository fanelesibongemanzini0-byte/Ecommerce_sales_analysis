
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "ecommerce_sales_cleaned.csv"
ENV_PATH = PROJECT_ROOT / ".env"

# Load environment variables
load_dotenv(ENV_PATH)

# Expected table structure
EXPECTED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product_category",
    "region",
    "quantity",
    "unit_price",
    "discount",
    "payment_method",
    "delivery_days",
    "customer_rating",
    "revenue",
]


def create_db_engine():
    """Create a connection to the MySQL database."""

    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        var for var in required_vars
        if os.getenv(var) is None
    ]

    if missing:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True,
    )


def load_data():
    """Validate the CSV and load it into MySQL."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    # Check the CSV structure
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "CSV columns do not match the expected schema."
        )

    if df.empty:
        raise ValueError("The cleaned CSV contains no records.")

    if df.isnull().any().any():
        raise ValueError("The cleaned CSV contains missing values.")

    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs found in the CSV.")

    # Standardize the date column
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="raise",
    ).dt.date

    engine = create_db_engine()

    try:
        # Test the database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("MySQL connection successful.")
        print(f"CSV records to load: {len(df)}")

        # Full refresh: replace existing sales records
        # and insert the cleaned CSV in one transaction.
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM sales"))

            df.to_sql(
                name="sales",
                con=connection,
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi",
            )

            loaded_count = connection.execute(
                text("SELECT COUNT(*) FROM sales")
            ).scalar_one()

            if loaded_count != len(df):
                raise RuntimeError(
                    f"Expected {len(df)} rows, "
                    f"but found {loaded_count}."
                )

        print("Data load completed successfully.")
        print(f"Records loaded: {loaded_count}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    load_data()
