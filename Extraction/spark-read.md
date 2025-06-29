In Spark 2.x and newer, `spark.read` is **not** a function you call like `spark.read()`. Rather, it's a **property** that returns a `DataFrameReader`—the entry point for reading data. 📘

---

## ✅ What `spark.read` Actually Is

> `spark.read` is a property (a `DataFrameReader` object), not a method—so you don’t call it with parentheses like `spark.read()`.([spark.apache.org][1])

That means the correct pattern is:

```python
df = spark.read.csv("path/to/file.csv")
df = spark.read.json("path/to/file.json")
df = spark.read.parquet("path/to/file.parquet")
```

---

## 📚 What You Can Do with It

Since `spark.read` gives you a `DataFrameReader`, you can chain options to customize how Spark reads data. For example:

```python
df = (
    spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/myfile.csv")
)

df2 = spark.read.format("json").load("path/to/mydata.json")
```

This allows flexible setups without needing to call a separate function for each format.

---

## 🧠 Difference from `spark.readStream`

* `.read` → **batch** processing: reads entire dataset at once.
* `.readStream` → **streaming** processing: reads incrementally, processing new data as it arrives.([stackoverflow.com][2])

---

## ✔️ TL;DR

✔ `spark.read` → **property** giving you a reader for files (CSV, JSON, Parquet, DB, etc.)
✔ You **don’t call** `spark.read()`; you call its methods (`.csv()`, `.json()`, `.parquet()`, or `.format(...).load(...)`)
✔ Use `.option()` or `.schema()` between `spark.read` and format method to customize behavior

---

### Example Usage

```python
# Create SparkSession as spark...

df = (
    spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/myfile.csv")
)

df.show()
```
---
spark.read.csv(...) is a shortcut method that internally calls spark.read.format("csv").load(...) 

Likewise, spark.read.parquet(...) is just a shorthand for spark.read.format("parquet").load(...) 

---
