import pandas as pd
from pathlib import Path
import sys


def validate_data():
    """Validate raw and cleaned product datasets."""

    project_root = Path(__file__).resolve().parent.parent

    raw_file = project_root / "data" / "raw" / "products_raw.csv"
    cleaned_file = project_root / "data" / "processed" / "products_cleaned.csv"

    print("\n========== DATA VALIDATION ==========")

    # Check that both files exist
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw dataset not found: {raw_file}")

    if not cleaned_file.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {cleaned_file}"
        )

    raw_df = pd.read_csv(raw_file)
    clean_df = pd.read_csv(cleaned_file)

    print(f"Raw rows: {len(raw_df)}")
    print(f"Cleaned rows: {len(clean_df)}")

    errors = []

    # 1. Check required columns
    required_columns = ["id", "price", "rating", "brand"]

    missing_columns = [
        column
        for column in required_columns
        if column not in clean_df.columns
    ]

    if missing_columns:
        errors.append(
            f"Required columns missing: {missing_columns}"
        )

    else:
        # 2. Check product IDs
        if clean_df["id"].isna().any():
            errors.append("Missing product IDs found.")

        if clean_df["id"].duplicated().any():
            errors.append("Duplicate product IDs found.")

        # 3. Check prices
        if clean_df["price"].isna().any():
            errors.append("Missing or invalid prices found.")

        if (clean_df["price"] < 0).any():
            errors.append("Negative prices found.")

        # 4. Check ratings
        if clean_df["rating"].isna().any():
            errors.append("Missing or invalid ratings found.")

        if (
            (clean_df["rating"] < 0)
            | (clean_df["rating"] > 5)
        ).any():
            errors.append("Ratings outside the 0–5 range found.")

        # 5. Check brands
        if clean_df["brand"].isna().any():
            errors.append("Missing brand values found.")

        if clean_df["brand"].astype(str).str.strip().eq("").any():
            errors.append("Blank brand values found.")

    # 6. Check duplicate rows
    duplicate_rows = clean_df.duplicated().sum()

    if duplicate_rows > 0:
        errors.append(
            f"{duplicate_rows} duplicate rows found."
        )

    # 7. Display results and fail if necessary
    if errors:
        print("\nVALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        raise ValueError(
            "Data validation failed. The pipeline must stop."
        )

    print("\nDuplicate rows: 0")
    print("Duplicate product IDs: 0")
    print("Missing product IDs: 0")
    print("Missing brands: 0")
    print("Invalid prices: 0")
    print("Invalid ratings: 0")
    print("\nVALIDATION PASSED")


if __name__ == "__main__":
    try:
        validate_data()
    except Exception as error:
        print(f"\nValidation error: {error}")
        sys.exit(1)