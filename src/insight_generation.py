
import pandas as pd
from pathlib import Path
from datetime import datetime


def generate_insights(df):
    """Generate business insights from cleaned product data."""

    insights = []

    # 1. Dataset overview
    insights.append("AUTOMATED BUSINESS INSIGHTS")
    insights.append("=" * 40)
    insights.append(f"Total products analyzed: {len(df)}")

    # 2. Category with the most products
    if "category" in df.columns and not df["category"].dropna().empty:
        category_counts = df["category"].value_counts()
        top_category = category_counts.idxmax()

        insights.append(
            f"Category with most products: {top_category} "
            f"({category_counts.max()} products)"
        )

    # 3. Category with the highest average price
    if {"category", "price"}.issubset(df.columns):
        average_prices = df.groupby("category")["price"].mean().dropna()

        if not average_prices.empty:
            category = average_prices.idxmax()
            insights.append(
                f"Highest average price category: {category} "
                f"({average_prices.max():.2f})"
            )

    # 4. Category with the highest average rating
    if {"category", "rating"}.issubset(df.columns):
        average_ratings = df.groupby("category")["rating"].mean().dropna()

        if not average_ratings.empty:
            category = average_ratings.idxmax()
            insights.append(
                f"Highest average rating category: {category} "
                f"({average_ratings.max():.2f}/5)"
            )

    # 5. Most expensive product
    if {"title", "price"}.issubset(df.columns):
        valid_prices = df.dropna(subset=["price"])

        if not valid_prices.empty:
            product = valid_prices.loc[valid_prices["price"].idxmax()]
            insights.append(
                f"Most expensive product: {product['title']} "
                f"({product['price']:.2f})"
            )

    # 6. Low-stock products
    if "stock" in df.columns:
        low_stock_count = (df["stock"] < 10).sum()
        insights.append(
            f"Products with stock below 10: {low_stock_count}"
        )

    # 7. Missing brand information
    if "brand" in df.columns:
        missing_brands = df["brand"].isna().sum()
        insights.append(
            f"Products with missing brand: {missing_brands}"
        )

    # 8. High-discount products with low ratings
    if {"discountPercentage", "rating", "title"}.issubset(df.columns):
        high_discount_low_rating = df[
            (df["discountPercentage"] >= 20)
            & (df["rating"] < 3.5)
        ]

        insights.append(
            f"Products with discount >= 20% and rating < 3.5: "
            f"{len(high_discount_low_rating)}"
        )

        for _, product in high_discount_low_rating.head(5).iterrows():
            insights.append(
                f"  - {product['title']}: "
                f"{product['discountPercentage']:.1f}% discount, "
                f"rating {product['rating']:.2f}/5"
            )

    # 9. Categories with the most low-stock products
    if {"category", "stock"}.issubset(df.columns):
        low_stock_products = df[df["stock"] < 10]

        if not low_stock_products.empty:
            low_stock_categories = low_stock_products["category"].value_counts()
            top_low_stock_category = low_stock_categories.idxmax()

            insights.append(
                f"Category with most low-stock products: "
                f"{top_low_stock_category} "
                f"({low_stock_categories.max()} products below 10 units)"
            )
        else:
            insights.append("Low-stock category analysis: No low-stock products found.")

    # 10. Unusually expensive products using the IQR method
    if "price" in df.columns:
        valid_prices = df["price"].dropna()

        if len(valid_prices) >= 4:
            q1 = valid_prices.quantile(0.25)
            q3 = valid_prices.quantile(0.75)
            iqr = q3 - q1
            upper_limit = q3 + (1.5 * iqr)

            expensive_outliers = df[
                df["price"] > upper_limit
            ].sort_values("price", ascending=False)

            insights.append(
                f"Potential high-price outliers: {len(expensive_outliers)} "
                f"(price above {upper_limit:.2f})"
            )

            for _, product in expensive_outliers.head(5).iterrows():
                insights.append(
                    f"  - {product.get('title', 'Unknown product')}: "
                    f"{product['price']:.2f}"
                )

    # 11. High-price categories with below-average ratings
    if {"category", "price", "rating"}.issubset(df.columns):
        category_summary = (
            df.groupby("category")
            .agg(
                average_price=("price", "mean"),
                average_rating=("rating", "mean"),
                product_count=("title", "count") if "title" in df.columns
                else ("price", "count")
            )
            .dropna(subset=["average_price", "average_rating"])
        )

        overall_average_price = df["price"].mean()
        overall_average_rating = df["rating"].mean()

        categories_to_review = category_summary[
            (category_summary["average_price"] > overall_average_price)
            & (category_summary["average_rating"] < overall_average_rating)
        ].sort_values("average_price", ascending=False)

        insights.append(
            f"Categories with above-average prices and below-average ratings: "
            f"{len(categories_to_review)}"
        )

        for category, row in categories_to_review.head(5).iterrows():
            insights.append(
                f"  - {category}: average price "
                f"{row['average_price']:.2f}, average rating "
                f"{row['average_rating']:.2f}/5"
            )

    return insights


def save_insights(insights):
    """Save insights to a timestamped text report."""

    project_root = Path(__file__).resolve().parent.parent
    reports_folder = project_root / "reports"
    reports_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = reports_folder / f"business_insights_{timestamp}.txt"

    with output_file.open("w", encoding="utf-8") as file:
        file.write("\n".join(insights))

    print("\n".join(insights))
    print(f"\nInsights saved to: {output_file}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    input_file = (
        project_root / "data" / "processed" / "products_cleaned.csv"
    )

    if not input_file.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {input_file}\n"
            "Run the data extraction and cleaning stages first."
        )

    df = pd.read_csv(input_file)

    insights = generate_insights(df)
    save_insights(insights)
