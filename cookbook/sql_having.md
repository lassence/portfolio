# The HAVING clause in SQL

Let's take the following table named `Orders` to illustrate our examples:

```
| OrderId | Customer | Amount | Items  |
|---------|----------|--------|--------|
| 1337    | Bob      | 25     | 1      |
| 1338    | Alice    | 70     | 3      |
| 1339    | Ted      | 59     | 4      |
| 1340    | Bob      | 12     | 1      |
| 1341    | Eric     | 63     | 2      |
| 1342    | Helen    | 10     | 1      |
| 1343    | Helen    | 75     | 2      |
| 1344    | David    | 77     | 5      |
| 1345    | Bob      | 66     | 4      |
| 1346    | Alice    | 37     | 2      |
```

In SQL, the `WHERE` clause filters row by row. For example:

```sql
SELECT *
  FROM Orders
 WHERE Amount >= 70
```

will return:

```
| OrderId | Customer | Amount | Items  |
|---------|----------|--------|--------|
| 1338    | Alice    | 70     | 3      |
| 1343    | Helen    | 75     | 2      |
| 1344    | David    | 77     | 5      |
```

## On grouped fields

The `HAVING` clause applies to fields that have been grouped or aggregated. You can apply it on a calculated field:

```sql
  SELECT Customer,
         SUM(Amount) AS TotalAmount
    FROM Orders
GROUP BY Customer
  HAVING TotalAmount >= 70
```

```
| Customer | Amount |
|----------|--------|
| Alice    | 107    |
| Bob      | 103    |
| David    | 77     |
| Helen    | 85     |
```

## With an aggregation function

It can also be used directly with an aggregation function, to calculate a condition on a field that is not returned in the result.

```sql
  SELECT Customer,
         SUM(Amount) AS TotalAmount
    FROM Orders
GROUP BY Customer
  HAVING COUNT(OrderId) >= 3
```
```
| Customer | Amount |
|----------|--------|
| Bob      | 103    |
```

## Combined with WHERE

A `HAVING` clause can be combined with a `WHERE` filter.

```sql
   SELECT Customer,
          SUM(Amount) AS TotalAmount
     FROM Orders
    WHERE Items > 1
 GROUP BY Customer
   HAVING TotalAmount >= 70
 ORDER BY TotalAmount DESC
```
```
| Customer | Amount |
|----------|--------|
| Alice    | 107    |
| Helen    | 85     |
| David    | 77     |
```

It must be positioned after `WHERE` and `GROUP BY`, and before `ORDER BY`.
