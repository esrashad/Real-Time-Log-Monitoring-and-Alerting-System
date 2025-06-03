from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_json, struct
from pyspark.sql.types import StructType, StringType


schema = StructType() \
    .add("timestamp", StringType()) \
    .add("level", StringType()) \
    .add("message", StringType())


spark = SparkSession.builder \
    .appName("KafkaLogConsumerBatch") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()


df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "logs") \
    .option("startingOffsets", "earliest") \
    .load()


df_parsed = df.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*")


error_logs = df_parsed.filter(col("level") == "ERROR")


error_logs.select(to_json(struct("*")).alias("value")) \
    .write \
    .mode("append") \
    .text("/app/output/error_logs")
