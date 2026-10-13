
import pandas as pd
from pathlib import Path


def load_raw_data():
    """Load the raw product dataset."""

    project_root = Path(__file__).resolve().parent.parent
    input_file = project_root / "data" / "raw" / "products_raw.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")

    return pd.read_csv(input_file)


def profile_data(df):
    """Check dataset structure and data quality."""

    print("\n========== DATASET OVERVIEW ==========")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")

    print("\n========== COLUMN NAMES ==========")
    print(df.columns.tolist())

    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== MISSING VALUES ==========")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values found.")

    print("\n========== DUPLICATE CHECKS ==========")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    if "id" in df.columns:
        print(f"Duplicate product IDs: {df['id'].duplicated().sum()}")
        print(f"Missing product IDs: {df['id'].isnull().sum()}")
    else:
        print("WARNING: The required 'id' column is missing.")

    print("\n========== BUSINESS RULE CHECKS ==========")

    if "price" in df.columns:
        print(f"Negative prices: {(df['price'] < 0).sum()}")

    if "discountPercentage" in df.columns:
        invalid = (
            (df["discountPercentage"] < 0)
            | (df["discountPercentage"] > 100)
        )
        print(f"Invalid discounts: {invalid.sum()}")

    if "rating" in df.columns:
        invalid = (df["rating"] < 0) | (df["rating"] > 5)
        print(f"Invalid ratings: {invalid.sum()}")

    print("\n========== NUMERICAL SUMMARY ==========")
    print(df.describe())


if __name__ == "__main__":
    print("Starting data profiling...")

    df = load_raw_data()
    profile_data(df)

    print("\nData profiling completed successfully!")
