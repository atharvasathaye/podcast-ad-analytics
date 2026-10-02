import os
from google.cloud import bigquery
import pandas as pd
from prophet import Prophet

# Setup BigQuery client
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
client = bigquery.Client(project=PROJECT_ID)

def extract_historical_revenue():
    # We aggregate revenue by day to feed into Prophet
    query = f"""
    SELECT 
        cast(payout_date as date) as ds, 
        sum(amount) as y
    FROM `{PROJECT_ID}.podcast_ad_analytics.fct_payouts`
    WHERE status = 'paid'
    GROUP BY 1
    ORDER BY 1
    """
    df = client.query(query).to_dataframe()
    return df

def generate_forecast(df):
    print("Training Prophet model on historical revenue...")
    m = Prophet(daily_seasonality=True, yearly_seasonality=False)
    m.fit(df)
    
    # Predict next 90 days
    future = m.make_future_dataframe(periods=90)
    forecast = m.predict(future)
    
    # Filter for only future dates
    future_forecast = forecast[forecast['ds'] > df['ds'].max()][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    future_forecast.columns = ['forecast_date', 'predicted_revenue', 'lower_bound', 'upper_bound']
    
    return future_forecast

def load_forecast_to_bq(forecast_df):
    table_id = f"{PROJECT_ID}.podcast_raw.revenue_forecast_90d"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )
    
    job = client.load_table_from_dataframe(
        forecast_df, table_id, job_config=job_config
    )
    job.result()
    print(f"Loaded {job.output_rows} forecasted rows to {table_id}")

if __name__ == "__main__":
    try:
        hist_df = extract_historical_revenue()
        if hist_df.empty:
            print("No historical data found. Skipping forecast.")
        else:
            forecast_df = generate_forecast(hist_df)
            load_forecast_to_bq(forecast_df)
    except Exception as e:
        print(f"Forecasting failed: {e}")
