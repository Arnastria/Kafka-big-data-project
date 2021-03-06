import airflow
from airflow import DAG
from airflow.operators import BashOperator
from datetime import timedelta

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=20)
}
dag1 = DAG(
    'rating_data_stream',  catchup=False, default_args=default_args, schedule_interval=timedelta(seconds=10))

bash_task = BashOperator(
    task_id='5s_rating_data',
    bash_command='python /usr/local/airflow/dags/app.py',
    dag=dag1
)

