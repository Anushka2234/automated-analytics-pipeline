import pandas as pd
from pathlib import Path


def load_raw_data():
    """Load the raw product dataset."""

    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "raw" / "products_raw.csv"

    df = pd.read_csv(input_file)

    return df


def clean_data(df):
    """Clean and prepare the product dataset."""

    # 1. Remove completely duplicate rows
    df = df.drop_duplicates()

    # 2. Remove duplicate product IDs
    df = df.drop_duplicates(subset=["id"])

    # 3. Handle missing brand values
    df["brand"] = df["brand"].fillna("Unknown")

    # 4. Clean text columns
    text_columns = [
        "title",
        "description",
        "category",
        "brand",
        "sku",
        "availabilityStatus",
        "returnPolicy"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    # 5. Make sure numeric columns have the correct data type
    numeric_columns = [
        "price",
        "discountPercentage",
        "rating",
        "stock",
        "weight",
        "minimumOrderQuantity"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # 6. Remove products with invalid IDs
    df = df.dropna(subset=["id"])

    return df


def save_cleaned_data(df):
    """Save the cleaned dataset."""

    project_root = Path(__file__).resolve().parent.parent

    output_folder = project_root / "data" / "processed"

    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "products_cleaned.csv"

    df.to_csv(output_file, index=False)

    print(f"\nCleaned data saved successfully to:")
    print(output_file)

    print(f"\nNumber of records after cleaning: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")


if __name__ == "__main__":

    print("Starting data cleaning...")

    df = load_raw_data()

    print(f"Records before cleaning: {len(df)}")

    df_cleaned = clean_data(df)

    save_cleaned_data(df_cleaned)

    print("\nData cleaning completed successfully!")