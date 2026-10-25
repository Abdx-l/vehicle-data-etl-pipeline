from datetime import datetime,timedelta
from airflow.decorators import dag,task
@dag(schedule="@daily",start_date=datetime(2026,1,1),catchup=False,default_args={"retries":2,"retry_delay":timedelta(minutes=1)})
def vehicle_etl():
 @task
 def extract():return "/opt/airflow/data/vehicle.csv"
 @task
 def validate_archive(source):
  from pipeline import process
  return process(source,"/opt/airflow/data/archive.parquet")
 @task
 def load_report(summary):
  import os,pandas as pd
  from sqlalchemy import create_engine
  from pipeline import load
  load(create_engine(os.environ["DATABASE_URL"]),pd.read_parquet("/opt/airflow/data/archive.parquet"),pd.DataFrame())
  return summary
 load_report(validate_archive(extract()))
vehicle_etl()
