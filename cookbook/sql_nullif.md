# Avoid division by zero errors in SQL

When calculating divisions in SQL, for example ratios, if the denominator value happens to be 0 in a row, the query will fail with a *Division By Zero* error.

To avoid this error and return a default value, use `NULLIF`.

`NULLIF(expr1, expr2)` will compare `expr1` with `expr2`. If they are equal, it will return *NULL*, which can be used to avoid a Division By Zero error.

```sql
WITH d AS (
  SELECT
    12 AS nom,
    0 AS denom
)

-- Avoid "Division by Zero" error
SELECT
  nom/NULLIF(denom, O) AS ratio
FROM d

-- Result
-- null
```
