import os
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud.exceptions import Conflict

# Load environment variables
load_dotenv()

# Initialize BigQuery client
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
dataset_id = os.getenv("BIGQUERY_DATASET")
table_id = os.getenv("BIGQUERY_TABLE")
region = os.getenv("GOOGLE_CLOUD_REGION")

client = bigquery.Client(project=project_id)

print(f"🔧 Setting up BigQuery for project: {project_id}")
print(f"📍 Region: {region} (Singapore)\n")

# Step 1: Create Dataset
dataset_ref = f"{project_id}.{dataset_id}"
dataset = bigquery.Dataset(dataset_ref)
dataset.location = region  # CRITICAL: Singapore region

try:
    dataset = client.create_dataset(dataset, timeout=30)
    print(f"✅ Created dataset: {dataset_ref}")
except Conflict:
    print(f"ℹ️  Dataset {dataset_ref} already exists")

# Step 2: Create Audit Table
table_ref = f"{project_id}.{dataset_id}.{table_id}"

schema = [
    bigquery.SchemaField("request_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("node_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("input_hash", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("output_hash", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("pdpa_flags", "STRING", mode="REPEATED"),  # Array of flags
    bigquery.SchemaField("ai_verify_principles", "STRING", mode="REPEATED"),
    bigquery.SchemaField("execution_time_ms", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("error_message", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("metadata", "JSON", mode="NULLABLE"),  # Flexible field
]

table = bigquery.Table(table_ref, schema=schema)

try:
    table = client.create_table(table)
    print(f"✅ Created table: {table_ref}")
    print(f"\n📋 Table schema:")
    for field in schema:
        print(f"   - {field.name} ({field.field_type})")
except Conflict:
    print(f"ℹ️  Table {table_ref} already exists")

print("\n🎯 BigQuery setup complete!")
print(f"💾 Data will be stored in: {region}")
print(f"🔍 View in console: https://console.cloud.google.com/bigquery?project={project_id}")