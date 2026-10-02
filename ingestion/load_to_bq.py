import os
import json
from google.cloud import bigquery

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    print("WARNING: GOOGLE_APPLICATION_CREDENTIALS is not set.")
    print("You must set this environment variable to load data into BigQuery.")
    
# To run this script successfully, update PROJECT_ID with your GCP project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
DATASET_ID = "podcast_raw"
OUTPUT_DIR = "data/raw"

def load_json_to_bq(client, table_name, file_path):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    # Read the JSON array and convert to NDJSON for BQ
    with open(file_path, "r") as f:
        data = json.load(f)
        
    ndjson_path = f"{file_path}.ndjson"
    with open(ndjson_path, "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")
            
    with open(ndjson_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    job.result()  # Waits for the job to complete.
    print(f"Loaded {job.output_rows} rows into {table_id}.")

if __name__ == "__main__":
    try:
        client = bigquery.Client(project=PROJECT_ID)
        
        # Create dataset if it doesn't exist
        dataset_ref = client.dataset(DATASET_ID)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
        
        files_to_load = [
            "podcasts", "episodes", "advertisers", 
            "campaigns", "downloads", "impressions", "payouts"
        ]
        
        for file in files_to_load:
            file_path = f"{OUTPUT_DIR}/{file}.json"
            if os.path.exists(file_path):
                load_json_to_bq(client, file, file_path)
            else:
                print(f"File {file_path} not found. Skipping.")
    except Exception as e:
        print(f"Failed to load data into BigQuery: {e}")
