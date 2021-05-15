# Using CASE in PostgreSQL

The basic usage of `CASE` is the following:

```sql
SELECT CASE WHEN Temperature < 0  THEN 'Cold'
            WHEN Temperature > 30 THEN 'Hot'
            ELSE 'Moderate'
       END
  FROM weather
```

If `ELSE` is omitted, a NULL will be returned if the value fall into the default case:

```sql
SELECT CASE WHEN Temperature < 0  THEN 'Cold'
            WHEN Temperature > 30 THEN 'Hot'
       END
  FROM weather
```

Also, when evaluating values of the same column on each `WHEN`, the column name can be stated just after `CASE`. With this method, only equality (`=`) can be tested, not intervals or greater/smaller.

```sql
SELECT CASE Department
            WHEN 'ACC' THEN 'Accounting'
            WHEN 'MKT' THEN 'Marketing'
            ELSE 'Other'
       END
  FROM employees
