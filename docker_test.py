from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.docker_operator import DockerOperator

with DAG(
    'nvidia_test',
    default_args={
        'depends_on_past': False,
        'email': ['kimjy.par@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': True,
        'retry': 3,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple nvidia gpu test',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021,8,10,22),
    catchup=False,
    tags=['nvidia'],
) as dag:
    t0 = BashOperator(
        task_id='bash_test',
        bash_command='echo hello bash operator'
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
