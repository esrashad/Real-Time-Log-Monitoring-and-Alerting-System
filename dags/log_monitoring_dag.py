from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='log_monitoring_dag',
    default_args=default_args,
    description='DAG for log producer, PySpark consumer, and alert system',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:


    start_log_producer = BashOperator(
        task_id='start_log_producer',
        bash_command='cd /opt/airflow/app && python -u log_producer.py'
    )

    start_spark_consumer = BashOperator(
        task_id='start_spark_consumer',
        bash_command='bash -c "echo Starting Spark Consumer && docker exec realtime_log_monitoring-spark-1 spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /app/log_consumer.py && echo Finished Spark Consumer"'
    )

    run_alert_script = BashOperator(
        task_id='run_alert_script',
        bash_command='python /opt/airflow/app/error_alert.py'
    )

    clean_old_logs = BashOperator(
        task_id='clean_old_logs',
        bash_command='find /opt/airflow/app/output/error_logs -type f -mmin +30 -delete'
    )

    
    start_log_producer >> start_spark_consumer >> run_alert_script >> clean_old_logs
