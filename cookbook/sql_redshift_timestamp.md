# Convert between epoch and datetime in Redshift

Redshift and PostgreSQL do not support native functions like MySQL's `FROM_UNIXTIME()` to convert Epoch time to a human-readable datetime.  

So we need to work around it with an inelegant solution that involves adding the number of seconds since 01/01/1970 to the Epoch timestamp:

```sql
-- Convert Epoch time to datetime
SELECT DATEADD(second, 1624654823, '1970-01-01') AS epoch_datetime
```

Conversely, to get the Epoch time from a proper datetime, we can use the following solution:

```sql
-- Convert datetime to Epoch timestamp
SELECT DATE_PART(epoch, '2021-06-25 21:00:23') as datetime_epoch
```
