You can read JSON files in PySpark using the `spark.read.json()` method from your SparkSession. Here’s how it works:

---

## 📥 Basic JSON Read

For newline-delimited JSON (default format):

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("JSONExample").getOrCreate()

df = spark.read.json("path/to/file.json")  # each line is a JSON object

df.printSchema()
df.show(5)

spark.stop()
```

Spark automatically infers the schema and loads it into a DataFrame ([sparkbyexamples.com][1], [spark.apache.org][2]).

---

## 🧩 Multi-line JSON Files

If your JSON records span multiple lines, enable the `multiLine` option:

```python
df = spark.read.option("multiLine", True).json("path/to/multiline.json")
```

This reads a JSON array or multi-line objects correctly ([sparktpoint.com][3], [pysparkguide.com][4]).

---

## 🌐 Reading Multiple Files or Folders

Load all JSON files in a folder or multiple paths:

```python
# All JSON in directory
df = spark.read.json("s3://bucket/json_data/")

# Multiple paths
df = spark.read.json(["file1.json", "file2.json", "folder3/"])
```

Spark merges them into a single DataFrame ([sparkbyexamples.com][1], [sparkcodehub.com][5]).

---

## 📝 Advanced Options & Custom Schema

* **Define custom schema** for more control and to improve performance:

  ```python
  from pyspark.sql.types import StructType, StructField, StringType, IntegerType

  schema = StructType([
      StructField("name", StringType(), True),
      StructField("age", IntegerType(), True),
  ])

  df = spark.read.schema(schema).json("data.json")
  ```
* Use other options like `mode`, `dateFormat`, or `allowComments` when needed ([stackoverflow.com][6], [spark.apache.org][7]).

---

## ✅ Why Use `spark.read.json`

* Convenient for semi-structured data
* Automatically handles nesting and arrays
* Schema inference or custom schemas work well with large datasets

---

## 🧪 Full Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.appName("JSONExample").getOrCreate()

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read \
    .option("multiLine", True) \
    .schema(schema) \
    .json("path/to/multiline_users.json")

df.show()
df.printSchema()

spark.stop()
```

---

### 👍 TL;DR

* Use `spark.read.json(...)` for standard JSON.
* Add `.option("multiLine", True)` for multi-line or array-formatted JSON.
* Specify schemas and other options for robust, large-scale processing.

