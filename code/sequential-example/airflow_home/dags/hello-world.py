from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Set default args
default_args = {
    'owner': 'dkhosla',
    'start_date': datetime(2018, 8, 22),
    'depends_on_past': False,
    'email': ['blabla@bla.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Declare Python Functions
def print_hello():
    return 'Hello!'


# Instantiate the dag
dag_1 = DAG(
    dag_id='dag_1',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
    )

# Instantiate Tasks
say_hello = PythonOperator(
    task_id='say_hello',
    python_callable=print_hello,
    dag=dag_1)

sleep = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    dag=dag_1)

print_date = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag_1)

dummy = DummyOperator(
    task_id='dummy',
    retries=2,
    dag=dag_1)

# Set up the DAG
say_hello >> sleep >> print_date
sleep >> dummy
