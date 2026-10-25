# Vehicle Data ETL Pipeline

Vehicle CSV validation, duplicate removal, reason-coded quarantine, PostgreSQL upserts, Parquet archival, and an Airflow DAG with retryable extract/validate/load stages.

## Run

Install requirements.txt. Run `python pipeline.py data/sample.csv --archive archive.parquet` for validation and archive. Set DATABASE_URL to load PostgreSQL after `psql -f schema.sql`. Airflow DAG is under dags/.
