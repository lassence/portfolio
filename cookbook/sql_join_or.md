# Join tables in SQL with multiple ON conditions

It is well known that tou can `JOIN` tables on multiple columns with `AND`:

```sql
SELECT a.id,
       a.first_name,
       a.last_name,
       a.team,
       b.age,
       b.score,
       b.team
  FROM table1 AS a
  JOIN table2 AS b
    ON a.id = b.id
   AND a.team = b.team
```

But you can also use `OR` in your join operation, if you have multiple possible columns for joining your tables:

```sql
SELECT a.id,
       a.first_name,
       a.last_name,
       a.team,
       b.age,
       b.score,
       b.team
  FROM table1 AS a
  JOIN table2 AS b
    ON a.id = b.id
    OR (LOWER(a.first_name) = LOWER(b.first_name)
        AND LOWER(a.last_name) = LOWER(b.last_name))
```

In this case, the join would be made in priority on `id`, then on `first_name ` and `last_name` as "fallback" option in case no match is found for IDs, but first and last names match.
