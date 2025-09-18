from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from fetch_api_script import fetch_data
from transform_data_script import transform_data
from load_to_db_script import load_data
from sql_reports_script import create_report


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 9, 17),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "crypto_etl",
    default_args=default_args,
    schedule_interval="@monthly",  # Runs every month
    catchup=False,
    max_active_runs=1,
) as dag:
    extract_task = PythonOperator(task_id="extract",
                                  python_callable=fetch_data,)
    
    transform_task = PythonOperator(task_id="transform", 
                                    python_callable=transform_data,)
        
    load_task = PythonOperator(task_id="load", 
                               python_callable=load_data,)
    
    create_report_task = PythonOperator(task_id="report", 
                               python_callable=create_report,)
    
    extract_task >> transform_task >> load_task >> create_report_task