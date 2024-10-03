from bigquery_setup import setup_bigquery_environment

# Set up the BigQuery environment
bq_config = setup_bigquery_environment()

# Use the configured environment
client = bq_config["client"]
project_id = bq_config["project_id"]
