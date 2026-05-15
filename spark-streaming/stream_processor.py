import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["hadoop.home.dir"] = "C:\\hadoop"

os.environ["PYSPARK_SUBMIT_ARGS"] = "--conf spark.hadoop.fs.defaultFS=file:/// pyspark-shell"

# Create Spark session
spark = SparkSession.builder \
    .appName("FraudDetectionStreamProcessor") \
    .master("local[*]") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka binary value to string
transactions = df.selectExpr("CAST(value AS STRING)")

# Print streaming data to console
query = df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", "false") \
    .option("checkpointLocation", "data/checkpoints") \
    .start()

query.awaitTermination()