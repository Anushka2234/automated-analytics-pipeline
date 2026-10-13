
from pathlib import Path
from datetime import datetime
from html import escape

import pandas as pd


# --------------------------------------------------
# 1. LOAD CLEANED PRODUCT DATA
# --------------------------------------------------

def load_data():
    """Load the cleaned product dataset."""

    project_root = Path(__file__).resolve().parent.parent

    data_file = (
        project_root
        / "data"
        / "processed"
        / "products_cleaned.csv"
    )

    if not data_file.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {data_file}\n"
            "Please run data cleaning before generating the report."
        )

    df = pd.read_csv(data_file)

    print(f"Loaded {len(df)} products successfully.")

    return df


# --------------------------------------------------
# 2. LOAD THE LATEST BUSINESS INSIGHTS
# --------------------------------------------------

def load_insights():
    """Load the latest business insights text file."""

    project_root = Path(__file__).resolve().parent.parent
    reports_folder = project_root / "reports"

    insight_files = sorted(
        reports_folder.glob("business_insights_*.txt"),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )

    if not insight_files:
        print("No business insights file found.")
        return []

    insight_file = insight_files[0]

    with insight_file.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    insights = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("="):
            continue

        if "AUTOMATED BUSINESS INSIGHTS" in line.upper():
            continue

        insights.append(line)

    print(f"Loaded business insights from: {insight_file.name}")

    return insights


# --------------------------------------------------
# 3. SAFE NUMERICAL CALCULATIONS
# --------------------------------------------------

def safe_mean(df, column):
    """Calculate the mean if the column contains valid numbers."""

    if column not in df.columns:
        return None

    values = pd.to_numeric(
        df[column],
        errors="coerce",
    ).dropna()

    if values.empty:
        return None

    return values.mean()


def safe_median(df, column):
    """Calculate the median if the column contains valid numbers."""

    if column not in df.columns:
        return None

    values = pd.to_numeric(
        df[column],
        errors="coerce",
    ).dropna()

    if values.empty:
        return None

    return values.median()


def format_number(value, decimals=2):
    """Format numbers consistently for the HTML report."""

    if value is None or pd.isna(value):
        return "N/A"

    return f"{value:,.{decimals}f}"


# --------------------------------------------------
# 4. CREATE KPI CARDS
# --------------------------------------------------

def create_kpi_card(label, value):
    """Generate the HTML for one KPI card."""

    return f"""
    <div class="kpi-card">
        <p class="kpi-label">{escape(str(label))}</p>
        <h2 class="kpi-value">{escape(str(value))}</h2>
    </div>
    """


# --------------------------------------------------
# 5. FIND CHARTS
# --------------------------------------------------

def find_charts(charts_folder):
    """Find up to three PNG charts."""

    chart_files = sorted(charts_folder.glob("*.png"))

    return chart_files[:3]


def create_chart_html(chart_files, project_root):
    """Generate HTML for the available chart images."""

    if not chart_files:
        return """
        <p class="notice">
            No PNG charts were found.
            Run EDA to generate visualizations.
        </p>
        """

    chart_html = []

    for chart_file in chart_files:
        relative_path = chart_file.relative_to(
            project_root
        ).as_posix()

        chart_title = chart_file.stem.replace("_", " ").title()

        chart_html.append(
            f"""
            <div class="chart-card">
                <h3>{escape(chart_title)}</h3>
                <img
                    src="../{escape(relative_path)}"
                    alt="{escape(chart_file.stem)}"
                    class="chart-image"
                >
            </div>
            """
        )

    return "\n".join(chart_html)


# --------------------------------------------------
# 6. FORMAT BUSINESS INSIGHTS
# --------------------------------------------------

def create_insights_html(insights):
    """
    Convert business insights into HTML.

    Normal lines become main bullet points.
    Lines beginning with a dash become nested sub-bullets
    under the preceding main insight.
    """

    main_insights = []

    for insight in insights:
        text = str(insight).strip()

        if not text:
            continue

        if text.startswith("="):
            continue

        if "AUTOMATED BUSINESS INSIGHTS" in text.upper():
            continue

        # Attach dash-prefixed details to the preceding insight.
        if text.startswith("-"):
            if main_insights:
                subitem = text.lstrip("- ").strip()

                main_insights[-1]["subitems"].append(subitem)

            continue

        # Store each main insight as a dictionary.
        main_insights.append(
            {
                "text": text,
                "subitems": [],
            }
        )

    if not main_insights:
        return """
        <li>
            No business insights are available yet.
            Run insight_generation.py first.
        </li>
        """

    insight_items = []

    for item in main_insights:
        main_text = escape(item["text"])
        subitems_html = ""

        if item["subitems"]:
            subitems_html = (
                '<ul class="insight-sublist">'
                + "".join(
                    f"<li>{escape(subitem)}</li>"
                    for subitem in item["subitems"]
                )
                + "</ul>"
            )

        insight_items.append(
            f"<li>{main_text}{subitems_html}</li>"
        )

    return "\n".join(insight_items)


# --------------------------------------------------
# 7. GENERATE THE HTML REPORT
# --------------------------------------------------

def generate_report(df, insights):
    """Generate a formatted HTML analytics report."""

    project_root = Path(__file__).resolve().parent.parent

    reports_folder = project_root / "reports"
    charts_folder = project_root / "charts"

    reports_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    charts_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    display_timestamp = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    # --------------------------------------------------
    # CALCULATE KPI VALUES
    # --------------------------------------------------

    total_products = len(df)

    average_price = safe_mean(df, "price")
    median_price = safe_median(df, "price")
    average_rating = safe_mean(df, "rating")
    average_discount = safe_mean(df, "discountPercentage")

    average_discount_text = (
        f"{format_number(average_discount)}%"
        if average_discount is not None
        else "N/A"
    )

    average_rating_text = (
        f"{format_number(average_rating)} / 5"
        if average_rating is not None
        else "N/A"
    )

    # --------------------------------------------------
    # BUILD KPI CARDS
    # --------------------------------------------------

    kpi_html = "".join(
        [
            create_kpi_card(
                "Total Products",
                f"{total_products:,}",
            ),
            create_kpi_card(
                "Average Price",
                format_number(average_price),
            ),
            create_kpi_card(
                "Median Price",
                format_number(median_price),
            ),
            create_kpi_card(
                "Average Rating",
                average_rating_text,
            ),
            create_kpi_card(
                "Average Discount",
                average_discount_text,
            ),
        ]
    )

    # --------------------------------------------------
    # BUILD BUSINESS INSIGHTS
    # --------------------------------------------------

    insight_html = create_insights_html(insights)

    # --------------------------------------------------
    # BUILD CHARTS
    # --------------------------------------------------

    chart_files = find_charts(charts_folder)

    charts_html = create_chart_html(
        chart_files,
        project_root,
    )

    # --------------------------------------------------
    # HTML DOCUMENT AND CSS
    # --------------------------------------------------

    html_content = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Automated Analytics Report</title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 30px;
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            color: #263238;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1180px;
            margin: auto;
        }}

        .header {{
            background: #19385f;
            color: white;
            padding: 35px 30px;
            border-radius: 14px;
            margin-bottom: 25px;
        }}

        .header h1 {{
            margin: 0 0 8px;
            font-size: 32px;
        }}

        .header p {{
            margin: 5px 0;
            font-size: 16px;
        }}

        .section {{
            background: white;
            border-radius: 14px;
            padding: 25px;
            margin: 25px 0;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
        }}

        .section h2 {{
            margin-top: 0;
            color: #19385f;
        }}

        /* KPI cards */

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 16px;
        }}

        .kpi-card {{
            background: white;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
            overflow-wrap: anywhere;
        }}

        .kpi-label {{
            margin: 0 0 12px;
            font-size: 15px;
            color: #526174;
        }}

        .kpi-value {{
            margin: 0;
            color: #1769aa;
            font-size: 25px;
        }}

        /* Business insights */

        .insight-list {{
            padding-left: 24px;
        }}

        .insight-list > li {{
            margin-bottom: 12px;
        }}

        .insight-sublist {{
            margin-top: 8px;
            padding-left: 28px;
            list-style-type: circle;
        }}

        .insight-sublist li {{
            margin-bottom: 6px;
            color: #526174;
        }}

        /* Charts */

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }}

        .chart-card {{
            border: 1px solid #e4eaf1;
            border-radius: 12px;
            padding: 15px;
            overflow: hidden;
        }}

        .chart-card h3 {{
            margin-top: 0;
            color: #19385f;
            font-size: 17px;
        }}

        .chart-image {{
            display: block;
            width: 100%;
            height: auto;
            object-fit: contain;
        }}

        /* Notifications */

        .notice {{
            color: #6b7280;
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
        }}

        /* Footer */

        .footer {{
            text-align: center;
            color: #6b7280;
            padding: 20px;
            font-size: 13px;
        }}

        /* Tablet layout */

        @media (max-width: 950px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Mobile layout */

        @media (max-width: 520px) {{
            body {{
                padding: 12px;
            }}

            .header {{
                padding: 24px 20px;
            }}

            .header h1 {{
                font-size: 25px;
            }}

            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .section {{
                padding: 18px;
            }}
        }}

        /* Print layout */

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .section,
            .kpi-card {{
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>

<body>
    <div class="container">

        <header class="header">
            <h1>Automated Analytics Report</h1>
            <p>Product Dataset Analysis</p>
            <p>Generated: {escape(display_timestamp)}</p>
        </header>

        <section class="kpi-grid">
            {kpi_html}
        </section>

        <section class="section">
            <h2>Key Business Insights</h2>

            <ul class="insight-list">
                {insight_html}
            </ul>
        </section>

        <section class="section">
            <h2>Data Visualizations</h2>

            <div class="charts-grid">
                {charts_html}
            </div>
        </section>

        <footer class="footer">
            <p>
                Automated Analytics Pipeline |
                Generated with Python and Pandas
            </p>

            <p>Report generated on {escape(display_timestamp)}</p>
        </footer>

    </div>
</body>

</html>
"""

    # --------------------------------------------------
    # SAVE THE REPORT
    # --------------------------------------------------

    output_file = (
        reports_folder
        / f"analytics_report_{timestamp}.html"
    )

    with output_file.open("w", encoding="utf-8") as file:
        file.write(html_content)

    print("\nHTML report generated successfully!")
    print(f"Report location: {output_file}")
    print(f"Products analyzed: {total_products}")
    print(f"Charts included: {len(chart_files)}")

    print("\nOpen the report in your browser:")
    print(output_file.resolve())

    return output_file


# --------------------------------------------------
# 8. RUN REPORT GENERATION
# --------------------------------------------------

if __name__ == "__main__":

    print("Starting HTML report generation...")

    try:
        df = load_data()
        insights = load_insights()

        generate_report(df, insights)

    except Exception as error:
        print(f"\nReport generation failed: {error}")
        raise
