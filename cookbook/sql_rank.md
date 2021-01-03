# Rank results in SQL with RANK, DENSE_RANK and ROW_NUMBER

When ranking rows in SQL, several functions may be used - `RANK()`, `DENSE_RANK()` and `ROW_NUMBER()` - in conjonction with windows, but they may generate different results.

As an example, let's use the following simple table:  

```
| id | employee | salary |
|----|----------|--------|
| 10 | Bob      | 45000  |
| 11 | Alice    | 65000  |
| 12 | Ted      | 45000  |
| 13 | Karen    | 52000  |
| 14 | Eric     | 63000  |
| 15 | Helen    | 45000  |
| 16 | Jim      | 65000  |
| 17 | David    | 67000  |
```

All three functions would return the same results if there is **no tie** between rows. However, they handle ties differently:  

* `RANK()` will assign the same number to all rows in a group of ties, and then "jump" and assign the number of preceding rows as rank for the next value - or group of equal values  
* `DENSE_RANK()` will increment rank by 1 at each group of identical values  
* `ROW_NUMBER()` does not handle ties, so each row will have a distinct consecutive number

```sql
SELECT id,
       employee,
       salary,
       RANK()       OVER (ORDER BY salary) AS rank,
       DENSE_RANK() OVER (ORDER BY salary) AS dense_rank,
       ROW_NUMBER() OVER (ORDER BY salary) AS row_number
  FROM employees
```

```
| id | employee | salary | rank | dense_rank | row_number |
|----|----------|--------|------|------------|------------|
| 15 | Helen    | 45000  | 1    | 1          | 1          |
| 12 | Ted      | 45000  | 1    | 1          | 2          |
| 10 | Bob      | 45000  | 1    | 1          | 3          |
| 13 | Karen    | 52000  | 4    | 2          | 4          |
| 14 | Eric     | 63000  | 5    | 3          | 5          |
| 11 | Alice    | 65000  | 6    | 4          | 6          |
| 16 | Jim      | 65000  | 6    | 4          | 7          |
| 17 | David    | 67000  | 8    | 5          | 8          |
```
