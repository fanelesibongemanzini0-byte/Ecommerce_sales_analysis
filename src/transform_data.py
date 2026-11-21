
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "ecommerce_sales_analytics_5000.csv"
)

PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_PATH = (
    PROCESSED_DIR / "ecommerce_sales_cleaned.csv"
)


def transform_data():
    # 1. Extract
    df = pd.read_csv(RAW_PATH)

    print(f"Raw records: {len(df)}")

    # 2. Transform data types
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="raise",
        format="mixed",
    )

    integer_columns = [
        "order_id",
        "customer_id",
        "quantity",
        "delivery_days",
    ]

    for column in integer_columns:
        df[column] = df[column].astype("int64")

    numeric_columns = [
        "unit_price",
        "discount",
        "customer_rating",
        "revenue",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

    # 3. Validate after transformation
    assert df["order_id"].is_unique
    assert df.isnull().sum().sum() == 0
    assert (df["quantity"] > 0).all()
    assert (df["unit_price"] > 0).all()
    assert df["discount"].between(0, 1).all()
    assert df["customer_rating"].between(1, 5).all()

    expected_revenue = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    ).round(2)

    assert (
        (df["revenue"] - expected_revenue).abs() <= 0.01
    ).all()

    # 4. Save processed data separately
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_PATH,
        index=False,
        date_format="%Y-%m-%d",
    )

    # 5. Report
    print("\n--- TRANSFORMATION REPORT ---")
    print(f"Processed records: {len(df)}")
    print(f"Output file: {PROCESSED_PATH}")
    print("\nUpdated data types:")
    print(df.dtypes)
    print("\nTransformation completed successfully.")


if __name__ == "__main__":
    transform_data()
