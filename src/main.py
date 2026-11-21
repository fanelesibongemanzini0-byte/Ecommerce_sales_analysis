import path
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR/"data"/"raw"/"ecommerce_sales_analytics_5000.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    print(f"the number of rows is {df.shape[0]}")
    print(f"the number of columns is {df.shape[1]}")

    print(df.head())

    print(df.dtypes)
    print(df.isnull().sum())
    print(df.duplicated().sum())
    dates = pd.to_datetime(df["order_date"], errors="coerce" )

    print(dates.min())
    print(dates.max())
    
    

    # 8. Data type validation
    print("\n8. DATA TYPES")
    print(df.dtypes)

    # 9. Categorical value inspection
    print("\n9. CATEGORICAL VALUES")

    categorical_columns = [
        "product_category",
        "region",
        "payment_method",
    ]

    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False))

    # 10. Numeric distribution checks
    print("\n10. NUMERIC DISTRIBUTIONS")

    numeric_columns = [
        "quantity",
        "unit_price",
        "discount",
        "delivery_days",
        "customer_rating",
        "revenue",
    ]

    print(df[numeric_columns].describe())

if __name__ == '__main__':
    main()


