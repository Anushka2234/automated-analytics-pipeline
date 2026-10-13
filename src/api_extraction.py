import requests
import pandas as pd
from pathlib import Path


# API endpoint
API_URL = "https://dummyjson.com/products"


def fetch_products():
    """Fetch all available products from the API using pagination."""

    all_products = []

    limit = 30
    skip = 0

    while True:

        response = requests.get(
            API_URL,
            params={
                "limit": limit,
                "skip": skip
            },
            timeout=30
        )

        # Stop if the API request fails
        response.raise_for_status()

        # Convert API response from JSON to Python dictionary
        data = response.json()

        products = data["products"]
        total = data["total"]

        all_products.extend(products)

        print(
            f"Fetched {len(products)} products | "
            f"Total fetched: {len(all_products)}/{total}"
        )

        # Stop when we have downloaded everything
        if len(all_products) >= total:
            break

        # Move to the next page
        skip += limit

    return all_products


def save_raw_data(products):
    """Save API data as a CSV file."""

    # Project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Raw data folder
    raw_folder = project_root / "data" / "raw"

    # Create folder if it doesn't exist
    raw_folder.mkdir(parents=True, exist_ok=True)

    # Convert data to DataFrame
    df = pd.DataFrame(products)

    # Save raw data
    output_file = raw_folder / "products_raw.csv"
    df.to_csv(output_file, index=False)

    print(f"Raw data saved successfully to: {output_file}")
    print(f"Number of records: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")


if __name__ == "__main__":

    print("Starting API data extraction...")

    products = fetch_products()

    save_raw_data(products)

    print("API extraction completed successfully!")