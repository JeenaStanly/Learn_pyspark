When you have a Spark session (`spark`) set up
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CSVExample").getOrCreate()
```
reading a CSV file is straightforward and powerful. Here’s how you do it:

---

### ✅ Basic CSV Read with Header

```python
df = spark.read \
    .option("header", "true") \
    .csv("path/to/1.csv")
```

This tells Spark:

* The first row is column names (`header=true`)
* Reads all files matching the path (even folders with multiple CSVs) ([bigdataschools.com][1], [thelinuxcode.com][2], [spark.apache.org][3])

---

### 🔧 Common Options to Customize Reading

* **`inferSchema`** to automatically detect column types:

  ```python
  .option("inferSchema", "true")
  ```
* **`delimiter`** for non-comma files (e.g., TSV):

  ````python
  .option("delimiter", "\t")
  ``` :contentReference[oaicite:7]{index=7}
  ````
* **`mode`** to control handling of bad records:

  ````python
  .option("mode", "PERMISSIVE")  # or FAILFAST, DROPMALFORMED
  ``` :contentReference[oaicite:9]{index=9}
  ````

---

---

### 📚 Why It Matters

* `header` tells Spark which row to use as column names
* `inferSchema` gives correct data types instead of default strings
* `delimiter` & `mode` make the parser robust for different file formats

---

