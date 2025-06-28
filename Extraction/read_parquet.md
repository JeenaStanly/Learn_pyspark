When using a **Parquet** file instead of CSV, the experience and performance in PySpark can be substantially better:

---

## 📊 1. Columnar Format & Column Pruning

Unlike CSV (row-based), **Parquet is columnar**—data for each column is stored together. Spark can read only the requested columns without scanning the entire file (projection pushdown).

---

## 🔍 2. Predicate Pushdown & Row-group Pruning

Parquet stores **metadata stats** (min/max per row group, optional bloom filters).
When you apply a filter like `filter(df.amount > 100)`, Spark uses this metadata to skip entire row groups that don’t satisfy the condition—significantly cutting I/O.

---

## 🛠 3. Partition Pruning (if partitioned)

If you've partitioned Parquet files by folder structure like `year=2025/month=06`, Spark can skip entire folders when filtering—similar to skipping chapters in a book.

---

## ⚡ 4. Performance vs CSV

| Feature            | CSV                   | Parquet                              |
| ------------------ | --------------------- | ------------------------------------ |
| Column Pruning     | ❌ reads all columns   | ✅ reads only needed ones             |
| Predicate Pushdown | ❌ no metadata         | ✅ leverages metadata to filter early |
| Compression        | plain text (larger)   | efficient, column-wise compression   |
| Schema Inference   | slower, less reliable | faster, structured metadata          |

With **CSV**, Spark reads every row and column (unless filtering happens later), resulting in more I/O and slower performance. Parquet, by contrast, reads only what’s needed—**much faster and cheaper** ([reddit.com][1], [cribl.io][4], [delta.io][5], [reddit.com][6]).

---

## 🧪 Quick Example

```python
df = spark.read.parquet("s3://bucket/data/")
df2 = (
    df.select("user_id", "amount", "year")
      .filter((df.year == 2025) & (df.amount > 100))
)
df2.show()
```

This triggers:

* ✅ **Partition pruning** (if folder-partitioned)
* ✅ **Column pruning** (reads only 3 columns)
* ✅ **Predicate pushdown** (only rows with `amount>100` are fetched)

---

## ✅ Summary

* **Parquet** ➕ **Partitioned folders** + **PySpark filters** = minimal data read.
* **CSV** reads everything—slow, heavy, and inefficient.
  For efficient big data workflows, Parquet is the recommended format.

---

