
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = (
    BASE_DIR / "data" / "raw" / "ecommerce_sales_analytics_5000.csv"
)


def validate_data(df):
    print("\n========== DATA QUALITY REPORT ==========")

    # 1. Dataset structure
    print("\n1. DATASET STRUCTURE")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # 2. Completeness
    print("\n2. MISSING VALUES")
    print(df.isnull().sum())
    print("Total missing values:", df.isnull().sum().sum())

    # 3. Uniqueness
    print("\n3. DUPLICATES")
    print("Duplicate rows:", df.duplicated().sum())
    print("Duplicate order IDs:", df["order_id"].duplicated().sum())

    # 4. Date validation
    print("\n4. DATE VALIDATION")
    dates = pd.to_datetime(df["order_date"], errors="coerce")

    print("Invalid dates:", dates.isna().sum())
    print("Earliest date:", dates.min())
    print("Latest date:", dates.max())
    print("Unique dates:", dates.nunique())

    # 5. Business rules
    print("\n5. BUSINESS RULES")

    checks = {
        "Invalid customer IDs": df["customer_id"] <= 0,
        "Invalid quantities": df["quantity"] <= 0,
        "Invalid unit prices": df["unit_price"] <= 0,
        "Invalid discounts": (
            (df["discount"] < 0) | (df["discount"] > 1)
        ),
        "Invalid delivery days": df["delivery_days"] < 0,
        "Invalid ratings": (
            (df["customer_rating"] < 1)
            | (df["customer_rating"] > 5)
        ),
        "Negative revenue": df["revenue"] < 0,
    }

    for name, condition in checks.items():
        print(f"{name}: {condition.sum()}")

    # 6. Revenue validation
    print("\n6. REVENUE VALIDATION")

    expected_revenue = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    ).round(2)

    revenue_difference = (
        df["revenue"] - expected_revenue
    ).abs()

    mismatches = revenue_difference > 0.01

    print("Revenue mismatches:", mismatches.sum())

    # 7. Date pattern investigation
    print("\n7. DATE PATTERN")

    sorted_dates = dates.dropna().sort_values()
    date_gaps = sorted_dates.diff().dropna()

    print(
        "One-day gaps:",
        (date_gaps == pd.Timedelta(days=1)).sum()
    )
    print("Total date gaps:", len(date_gaps))

    print("\n========== VALIDATION COMPLETE ==========")


def main():
    df = pd.read_csv(DATA_PATH)
    validate_data(df)


if __name__ == "__main__":
    main()
