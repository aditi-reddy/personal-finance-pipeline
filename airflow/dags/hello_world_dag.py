"""
Hello World DAG - First Airflow Pipeline
Author: Aditi Reddy
Purpose: Learn Airflow basics
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    'owner': 'aditi',
    'depends_on_past': False,
    'email': ['aditi.reddy@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Python functions for tasks
def print_hello():
    print("Hello from Airflow!")
    print("This is my first DAG running successfully!")
    return "Hello task completed"

def print_date():
    current_time = datetime.now()
    print(f"Current date and time: {current_time}")
    print(f"DAG is working perfectly!")
    return "Date task completed"

def print_goodbye():
    print("Pipeline finished successfully!")
    print("Ready to build ETL pipelines!")
    return "Goodbye task completed"

# Define the DAG
with DAG(
    dag_id='hello_world_pipeline',
    default_args=default_args,
    description='My first Airflow DAG - Hello World',
    schedule=None,  # Changed from schedule_interval to schedule in Airflow 3.x
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['tutorial', 'hello-world', 'day-2'],
) as dag:

    # Task 1: Print Hello
    task_hello = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    # Task 2: Print Date
    task_date = PythonOperator(
        task_id='print_date',
        python_callable=print_date,
    )

    # Task 3: Print Goodbye
    task_goodbye = PythonOperator(
        task_id='print_goodbye',
        python_callable=print_goodbye,
    )

    # Define task dependencies (execution order)
    task_hello >> task_date >> task_goodbye