To read a **Parquet** file in PySpark, you use the `spark.read.parquet(...)` method from your `SparkSession`. Here’s how it works:

---

## 📦 Reading a Parquet File – Simple Example

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParquetExample") \
    .getOrCreate()

df = spark.read.parquet("path/to/your/file.parquet")

df.printSchema()
df.show(5)

spark.stop()
```

* **Self-describing**: Parquet files contain embedded schema, so Spark automatically applies it when reading ([sparkbyexamples.com][1], [spark.apache.org][2]).
* **Flexible paths**: You can point to a single file, a directory, or use wildcards like `"folder/*.parquet"` ([sparkcodehub.com][3]).

---

## 🧰 Advanced Options

### 1. Read multiple files or directories:

```python
df = spark.read.parquet("folder1/", "folder2/")
```

Or with wildcard:

```python
df = spark.read.parquet("folder/*.parquet")
```

Spark consolidates them into a single DataFrame ([sparkcodehub.com][3]).

### 2. Merge schemas across different files:

```python
df = spark.read.option("mergeSchema", "true") \
               .parquet("path/to/parquet_files/")
```

Useful when files may have evolved schemas ([mainri.ca][4]).

### 3. Select specific columns (column pruning):

```python
df = spark.read.parquet("data/").select("name", "age")
```

Spark reads only those columns—great for performance .

---

## ✅ Key Benefits of Parquet

| Feature                   | Description                                  |
| ------------------------- | -------------------------------------------- |
| **Columnar storage**      | Reads only needed columns                    |
| **Predicate pushdown**    | Uses metadata to skip unnecessary row groups |
| **Auto schema detection** | No need to define schema manually            |
| **Partition discovery**   | Can infer partitions via folder structure    |

All these result in **faster reads**, **less I/O**, and **lower compute costs** ([sparkcodehub.com][3], [mainri.ca][4]).

---

## 🧪 Full Example with Options

```python
df = (
    spark.read
        .option("mergeSchema", "true")
        .parquet("s3://your-bucket/data/")
)

df.select("user_id", "year", "amount") \
  .filter(df.year == 2025) \
  .show()
```

---

### TL;DR

To read Parquet in PySpark:

```python
df = spark.read.parquet("path/to/parquet")
```

Add `.option("mergeSchema", "true")` if you're combining files with different schemas. Use `.select()` and `.filter()` to optimize performance via pruning.
