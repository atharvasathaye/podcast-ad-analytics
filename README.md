# Podcast Ad Marketplace Analytics

An end-to-end data engineering and analytics pipeline for a podcast ad marketplace, modeled after platforms like RedCircle or Midroll. 

This project ingests real podcast metadata and synthesizes realistic ad campaign transactions. It transforms the raw events into actionable business intelligence using dbt and BigQuery, and generates revenue forecasts.

> **Note**: The ad campaign events, impressions, and payouts in this dataset are *synthetic*. They were generated using Python (`Faker` and `NumPy`) for demonstration purposes.

## Architecture

1. **Ingestion Layer (Python)**: Fetches real podcast data from the iTunes Search API and generates synthetic events.
2. **Data Warehouse (BigQuery)**: Stores raw, staging, and modeled data.
3. **Transformation Layer (dbt)**: Cleans, tests, and models the data into dimension, fact, and mart tables.
4. **Forecasting (Prophet)**: Predicts future revenue based on historical data.
5. **Orchestration (GitHub Actions)**: Automates the pipeline with a daily scheduled run and PR checks.

## Setup Instructions

### 1. Prerequisites
- A Google Cloud Platform (GCP) account.
- A BigQuery project (free tier is sufficient).
- A Service Account with BigQuery Admin privileges. Download the JSON key.

### 2. Local Setup
1. Clone this repository.
2. Set your environment variables:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
   export GCP_PROJECT_ID="your-gcp-project-id"
   ```
3. Run the ingestion scripts:
   ```bash
   pip install -r ingestion/requirements.txt
   python ingestion/extract_itunes.py
   python ingestion/generate_events.py
   python ingestion/load_to_bq.py
   ```
4. Run dbt:
   ```bash
   cd dbt_project
   dbt deps
   dbt build
   dbt snapshot
   ```
5. (Optional) Run the forecaster:
   ```bash
   cd ../forecasting
   pip install -r requirements.txt
   python forecast_revenue.py
   ```

### 3. CI/CD setup
To enable GitHub actions, add the following secrets to your GitHub repository:
- `GCP_PROJECT_ID`: Your GCP project ID.
- `GCP_CREDENTIALS`: The raw JSON content of your service account key.

## Data Quality & Testing
This project uses generic and custom singular dbt tests to catch deliberate anomalies planted during the synthetic data generation (e.g. duplicate downloads, missing listener IDs). Tests will assert that impressions never exceed downloads and that payouts reconcile perfectly.
