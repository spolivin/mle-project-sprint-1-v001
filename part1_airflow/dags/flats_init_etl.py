import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator

from steps.real_estate import create_table, extract, load
from steps.messages import send_telegram_success_message, send_telegram_failure_message


with DAG(
    dag_id="flats_init_etl",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule="@once",
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
    tags=["ETL", "Stage-1", "Data-collection"],
) as dag:
    create_table_step = PythonOperator(
        task_id="create_table", python_callable=create_table
    )
    extract_step = PythonOperator(task_id="extract", python_callable=extract)
    load_step = PythonOperator(task_id="load", python_callable=load)

    create_table_step >> extract_step
    extract_step >> load_step
