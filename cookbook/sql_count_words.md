# Count words and characters in a string with PostgreSQL

## Count words

```sql
/* Count words separated by whitespaces */
SELECT ARRAY_LENGTH(REGEXP_SPLIT_TO_ARRAY(string_field, '\s'), 1)
  FROM your_table
```

## Count characters

```sql
/* Count characters */
SELECT SUM(LENGTH(string_field))
  FROM your_table
```
