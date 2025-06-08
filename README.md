# Real-Time Log Monitoring and Alerting System
IWD Final Project – Data Engineering Track

This project is a real-time log monitoring and alerting system using Apache Kafka, Apache Spark, Apache Airflow, and Python. The system ingests logs, filters error logs, stores them in JSON format, and triggers alerts when critical errors are detected.

---

## 📷 Solution Architecture

![Untitled Diagram drawio (4)](https://github.com/user-attachments/assets/14d160c6-37f3-48f7-a2f2-cdd976553efb)


---

## ⚙️ Technologies Used

* **Apache Kafka** (Confluent): Real-time log streaming.
* **Apache Spark (Bitnami)**: PySpark for log filtering and processing.
* **Apache Airflow**: Workflow orchestration.
* **Docker & Docker Compose**: Containerization and environment setup.
* **Python**: Log producer, log consumer, and alerting scripts.

---

## 🚀 Project Steps

### 1. Environment Setup

* Install Docker and Docker Compose.
* Clone the project repository.
* Build and start the environment:

  ```bash
  docker-compose up -d --build
  ```

### 2. Create Kafka Topic

* Access the Kafka container:

  ```bash
  docker exec -it real_time_log_monitoring-kafka-1 bash
  ```
* Create a topic:

  ```bash
  kafka-topics --create \
    --topic logs \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
  ```

### 3. Run Log Producer

* Generates simulated log messages and sends them to Kafka.
* Script: `log_producer.py`
* Usage:

  ```bash
  docker exec -it real_time_log_monitoring-airflow-1 python log_producer.py
  ```

### 4. Run PySpark Log Consumer

* Consumes logs from Kafka and filters error logs.
* Stores the filtered logs as JSON.
* Script: `log_consumer.py`
* Usage:

  ```bash
  docker exec -it real_time_log_monitoring-pyspark-client-1 \
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 log_consumer.py
  ```

### 5. Alerting System

* Scans the filtered logs for critical errors.
* Sends alerts (e.g., prints messages or can be extended to email/SMS).
* Script: `alerting.py`
* Usage:

  ```bash
  docker exec -it real_time_log_monitoring-airflow-1 python alerting.py
  ```

### 6. Airflow DAG

* Orchestrates the entire pipeline.
* DAG file: `log_monitoring_dag.py`
* Trigger via Airflow UI or CLI:

  ```bash
  airflow dags trigger log_monitoring_dag
  ```

---

## 📁 Project Structure

```
real_time_log_monitoring/
│
├── docker-compose.yml
├── Dockerfile
├── log_producer.py
├── log_consumer.py
├── alerting.py
├── dags/
│   └── log_monitoring_dag.py
├── output/
│   └── error_logs.json
└── solution_architecture.png
```

---

## ✅ Output

* JSON file with filtered error logs: `output/error_logs.json`
* Console alerts for critical logs.

---

## 📄 License

[MIT License](./LICENSE)
