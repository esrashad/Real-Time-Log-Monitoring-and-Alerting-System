FROM apache/airflow:2.10.1

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt
