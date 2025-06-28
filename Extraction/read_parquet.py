from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParquetExample") \
    .getOrCreate()

df = spark.read.parquet("path/to/your/file.parquet")

df.printSchema()
df.show(5)

spark.stop()
