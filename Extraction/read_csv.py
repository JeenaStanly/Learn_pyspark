from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CSVExample").getOrCreate()

df = (
    spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .option("delimiter", ",")
      .option("mode", "PERMISSIVE")
      .csv("s3://your-bucket/data/1.csv")
)

df.printSchema()
df.show(5)

spark.stop()
