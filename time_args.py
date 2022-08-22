from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.docker_operator import DockerOperator

with DAG(
    'time_args_test',
    default_args={
        'depends_on_past': False,
        'email': ['kimjy.par@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': True,
        'retry': 3,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple nvidia gpu test',
    schedule_interval='*/5 * * * *',
    start_date=datetime(2021,8,22,8),
    catchup=False,
    tags=['nvidia'],
) as dag:
    data_interval_start = "{{ data_interval_start }}" 
    data_interval_end = "{{ data_interval_end }}"
    t0 = BashOperator(
        task_id='bash_test',
        bash_command='echo hello bash operator {} - {}'.format(data_interval_start, data_interval_end)
    )
 
    t1 = DockerOperator(
        task_id='docker_test',
        image='ubuntu:18.04',
        api_version='auto',
        auto_remove=True,
        command='echo hello docker operator',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

    t0>>t1
