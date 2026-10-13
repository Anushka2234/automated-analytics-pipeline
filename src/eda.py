import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_cleaned_data():
    """Load the cleaned product dataset."""

    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "processed" / "products_cleaned.csv"

    df = pd.read_csv(input_file)

    return df


def basic_statistics(df):
    """Calculate basic business statistics."""

    print("\n========== BASIC STATISTICS ==========")

    print(f"Total products: {len(df)}")

    print(f"Average price: {df['price'].mean():.2f}")

    print(f"Median price: {df['price'].median():.2f}")

    print(f"Average discount: {df['discountPercentage'].mean():.2f}%")

    print(f"Average rating: {df['rating'].mean():.2f}")

    print(f"Total stock: {df['stock'].sum()}")

    print(f"Average stock per product: {df['stock'].mean():.2f}")

    print(
        f"Average minimum order quantity: "
        f"{df['minimumOrderQuantity'].mean():.2f}"
    )


def category_analysis(df):
    """Analyze products by category."""

    print("\n=======CATEGORY ANALYSIS ========")

    #Number of products in each category
    category_counts = df["category"].value_counts()

    print("\nProducts by category:")
    print(category_counts)


    #Average price by category
    category_price = (
        df.groupby("category")["price"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nAverage Price by category:")
    print(category_price.round(2))

    #Average rating by category
    category_rating = (
        df.groupby("category")["rating"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nAverage rating by category:")
    print(category_rating.round(2))

def create_visualizations(df):
    """Create and save EDA charts."""

    project_root = Path(__file__).resolve().parent.parent
    charts_folder = project_root / "charts"
    charts_folder.mkdir(parents=True, exist_ok=True)

    #1.Number of products by category
    product_counts = df["category"].value_counts()

    plt.figure(figsize=(12,7))
    product_counts.sort_values().plot(kind="barh")
    plt.title("Number of Products by Category")
    plt.xlabel("Number of Products")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(charts_folder / "products_by_category.png",dpi=150)
    plt.close()

    #Average Price by category
    avg_prices = df.groupby("category")["price"].mean().sort_values()

    plt.figure(figsize=(12,7))
    avg_prices.plot(kind="barh")
    plt.title("Average Product Price by Category")
    plt.xlabel("Average Price")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(charts_folder / "average_price_by_category.png", dpi=150)
    plt.close()

    # 3. Average rating by category
    avg_ratings = df.groupby("category")["rating"].mean().sort_values()

    plt.figure(figsize=(12, 7))
    avg_ratings.plot(kind="barh")
    plt.title("Average Product Rating by Category")
    plt.xlabel("Average Rating")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(charts_folder / "average_rating_by_category.png", dpi=150)
    plt.close()

    print(f"\nCharts saved successfully in: {charts_folder}")

if __name__ == "__main__":

    print("Starting EDA...")

    df = load_cleaned_data()

    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")

    basic_statistics(df)
    category_analysis(df)
    create_visualizations(df)

    print("\nEDA completed successfully!")