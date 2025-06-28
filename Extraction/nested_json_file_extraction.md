Let’s walk through a concrete example where your JSON has a nested **address** structure and you want to flatten it in PySpark.

---

## 📘 Sample JSON (`users.json`)

```json
[
  {
    "user_id": 1,
    "name": "Alice",
    "address": {
      "street": "123 Main St",
      "city": "Springfield",
      "zip": "11111"
    },
    "orders": [
      { "order_id": 101, "amount": 250 },
      { "order_id": 102, "amount": 40 }
    ]
  },
  {
    "user_id": 2,
    "name": "Bob",
    "address": {
      "street": "456 Oak Ave",
      "city": "Shelbyville",
      "zip": "22222"
    },
    "orders": [
      { "order_id": 103, "amount": 75 }
    ]
  }
]
```

---

## 🚀 PySpark Code to Flatten

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

spark = SparkSession.builder.appName("FlattenJSON").getOrCreate()

df = spark.read.option("multiLine", True).json("users.json")
```

### 1. Extract address fields

```python
df1 = df.select(
    "user_id",
    "name",
    col("address.street").alias("street"),
    col("address.city").alias("city"),
    col("address.zip").alias("zip")
)
```

### 2. Flatten orders array

```python
df2 = df1.join(
    df.select("user_id", explode(col("orders")).alias("order")),
    on="user_id"
)

df_final = df2.select(
    "user_id", "name", "street", "city", "zip",
    col("order.order_id").alias("order_id"),
    col("order.amount").alias("order_amount")
)

df_final.show(truncate=False)
```

---

## ✅ Output (flattened)

```
+-------+-----+------------+------------+-----+--------+------------+
|user_id|name |street      |city        |zip  |order_id|order_amount|
+-------+-----+------------+------------+-----+--------+------------+
|1      |Alice|123 Main St |Springfield |11111|101     |250         |
|1      |Alice|123 Main St |Springfield |11111|102     |40          |
|2      |Bob  |456 Oak Ave |Shelbyville |22222|103     |75          |
+-------+-----+------------+------------+-----+--------+------------+
```

---

## 🔧 How It Works

1. **Dot notation** (`address.street`) pulls values from nested structs.
2. **`explode()`** converts each element of the orders array into separate rows.
3. **`.select()`** lets you reshape and alias nested fields easily.

---

### 🧠 Bonus: Automate Flattening

For unknown nested structures, you can use a dynamic function to flatten:

```python
from pyspark.sql.types import StructType
def flatten_df(nested_df):
    # find struct and array types, explode arrays and flatten structs...
    # (Refer to dynamic flatten logic from StackOverflow)
    ...
```

This automatically handles multi-level nested JSON.

---
