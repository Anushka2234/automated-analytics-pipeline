# Automated Analytics Pipeline

An end-to-end Python analytics project that automatically extracts product data from a public API, profiles and cleans the dataset, validates data quality, performs exploratory data analysis, generates business insights, and produces a shareable HTML report.

## Project Overview

The objective of this project is to reduce repetitive manual work in data analysis by combining data extraction, data preparation, analytics, visualization, and reporting into one automated workflow.

The pipeline can be executed manually using Python or scheduled weekly through Windows Task Scheduler.

## Key Features

- **API Data Extraction:** Retrieves product data from a public API.
- **Data Profiling:** Examines dataset structure, columns, missing values, and data characteristics.
- **Data Cleaning:** Prepares the extracted data for analysis.
- **Data Validation:** Checks for duplicate records, missing identifiers, invalid values, and other data-quality issues.
- **Exploratory Data Analysis (EDA):** Analyzes product prices, ratings, categories, and other available attributes.
- **Business Insight Generation:** Identifies top categories, expensive products, low-stock products, and other useful patterns.
- **Data Visualization:** Generates charts for product category counts, average prices, and ratings.
- **HTML Report Generation:** Creates a shareable report containing summary metrics, insights, and charts.
- **Logging and Error Handling:** Records execution details and helps identify failed pipeline stages.
- **Scheduled Execution:** Supports weekly automated execution through Windows Task Scheduler.

## Pipeline Architecture

```text
Public Product API
        |
        v
API Extraction
        |
        v
Data Profiling
        |
        v
Data Cleaning
        |
        v
Data Validation
        |
        v
Exploratory Data Analysis
        |
        v
Business Insight Generation
        |
        v
Chart and HTML Report Generation
        |
        v
Logs and Reports
```

## Technology Stack

- **Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib
- **API Integration:** Requests
- **Data Validation:** Python and Pandas
- **Reporting:** HTML, CSS, Python
- **Database Integration Libraries:** SQLAlchemy and pyodbc installed for potential SQL integration
- **Automation:** Windows Task Scheduler and Windows batch scripting
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## Project Structure

```text
Automated_Analytics_Pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── api_extraction.py
│   ├── data_profiling.py
│   ├── data_cleaning.py
│   ├── validate_data.py
│   ├── eda.py
│   ├── insight_generation.py
│   └── report_generation.py
├── charts/
├── reports/
├── logs/
├── main.py
├── run_pipeline.bat
├── requirements.txt
├── .gitignore
└── README.md
```

## Example Output

The pipeline generates an HTML analytics report with:

- Total products analyzed
- Average and median product prices
- Average product rating and discount
- Key business insights
- Average price by category
- Average rating by category
- Number of products by category

Execution logs are saved separately to support monitoring and troubleshooting.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Anushka2234/automated-analytics-pipeline.git
cd automated-analytics-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment on Windows

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use a suitable temporary execution policy for the current terminal session.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the pipeline

```bash
python main.py
```

After successful execution, check the `reports/` folder for the generated HTML report and the `logs/` folder for execution logs.

## Automated Scheduling

The pipeline can be scheduled using Windows Task Scheduler. A batch file activates the virtual environment, runs `main.py`, and redirects console output to a scheduler log.

The configured schedule is weekly on Sunday at 10:00 AM.

## Data Quality and Reliability

The pipeline includes a validation stage and stops execution when a stage fails. Logs capture execution details to make debugging easier.

## Future Enhancements

- Integrate Python with a SQL database for persistent storage.
- Add incremental extraction and API pagination.
- Introduce configurable data-quality rules.
- Add email notifications after successful or failed runs.
- Deploy the reporting workflow to a cloud environment.
- Integrate AI-assisted business insight generation.

## Author

**Anushka Srivastava**

Data Analytics | Python | SQL | Power BI | Data Engineering Projects

GitHub: https://github.com/Anushka2234

---

*This project was developed as a hands-on capstone to demonstrate an automated, end-to-end analytics workflow.*
