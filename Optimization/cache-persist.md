## 🔁 Lazy Evaluation: What Really Happens

1. You create a DataFrame:

   ```python
   df = spark.read.csv("s3://bucket/file.csv")
   df.show()
   ```

   * `.show()` triggers reading the file from S3
   * Spark builds up your transformations in a query plan but **does not store** the data after `.show()`

2. You apply more transformations:

   ```python
   df2 = df.select("col1", "col2")
   df2.count()
   ```

   * `df2.count()` triggers **re-reading** the CSV from S3, applying the `select` step again

---

## ⚙️ Why This Happens

* Spark **records transformations** (map, select, filter) lazily—no actual execution
* Only when you execute an **action** (e.g. `count()`, `show()`, `write()`) does Spark:

  * Read the data from S3
  * Apply your transformations
  * Return results

Every action causes Spark to **replay the entire lineage** from the original read—unless you cache the DataFrame ([stackoverflow.com][1], [data-flair.training][2], [deep-dive-data.com][3], [sparktpoint.com][4], [stackoverflow.com][5], [stackoverflow.com][6]).

---

## 🛠️ How to Avoid Repeated Reads: `cache()` or `persist()`

To prevent re-scanning your source for each action:

```python
df = spark.read.csv("s3://bucket/file.csv")
df2 = df.select("col1", "col2").cache()  # mark for caching

df2.count()  # triggers S3 read + transformations + storage in cache
df2.show()   # now uses the in-memory cache—no re-scan from S3
df2.filter(...).count()  # also uses cached data
```

By caching after your transformations, Spark avoids redundant work:

* **Transforms** are only computed **once at the first action**
* **Subsequent actions** read from the in-memory (or disk) cache—fast and efficient ([sparktpoint.com][4], [sparkbyexamples.com][7])

---

## ✅ Best Practices for Caching

| Scenario                    | Use Case                                     |
| --------------------------- | -------------------------------------------- |
| Multiple actions on same DF | ✅ Use `.cache()` or `.persist()`             |
| One-off action only         | ❌ No caching needed                          |
| Large DF, limited memory    | Use `.persist(StorageLevel.MEMORY_AND_DISK)` |
| After done using cached DF  | Call `df2.unpersist()` to free resources     |

---

## 🔍 TL;DR

* **Any action** (show, count, write) causes a full lineage execution
* **Cache or persist** after transformations only if the DataFrame will be reused
* **Trigger cache** with an action, then follow-up operations will not re-read from S3

