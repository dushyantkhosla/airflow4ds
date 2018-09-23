import sys
import os

PROJECT_DIRECTORY = os.getenv(key='AIRFLOW_HOME')
sys.path.append(PROJECT_DIRECTORY)

from src import get_raw_iris, get_clean_iris

import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'start_date': dt.datetime(2018, 8, 22),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('airflow_tutorial_v01',
         default_args=default_args,
         schedule_interval='0 0 * * *',
         ) as dag:

    print_hello = BashOperator(task_id='print_hello', bash_command='echo "hello"')

    sleep = BashOperator(task_id='sleep', bash_command='sleep 5')

    get_data = PythonOperator(task_id='get_raw_iris', python_callable=get_raw_iris)

    clean_data = PythonOperator(task_id='get_clean_iris', python_callable=get_clean_iris)

print_hello >> sleep >> get_data >> clean_data
