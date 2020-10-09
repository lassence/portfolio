# Time intervals in PostgreSQL

Calculating differences between dates and datetimes has different flavors in SQL.
Let's just say that PostgreSQL is not the most elegant or well-equipped language for this matter.

## Behaviour for dates and timestamps

Substracting **timestamps** will give a time interval:

```sql
WITH d AS (
    SELECT
        '2020-01-01 10:09:00'::timestamp AS start_date,
        '2020-05-15 13:37:00'::timestamp AS end_date
)

SELECT
    end_date - start_date
FROM d

-- Result
-- 135 days 03:28:00
```

While substracting **dates** will directly give the time delta in days:

```sql
WITH d AS (
    SELECT
        '2020-01-01 10:09:00'::date AS start_date,
        '2020-05-15 13:37:00'::date AS end_date
)

SELECT
    end_date - start_date
FROM d

-- Result
-- 135
```

## Interval in days

Depending on the points in time you want to compare being dates or timestamps, there are two options to calculate the interval in days:

```sql
SELECT
    -- Option 1: convert to dates and substract
    end_date::date - start_date::date AS days_date,
    -- Option 2: substract timestamps and extract days
    DATE_PART('day', end_date - start_date) AS days_timestamp
FROM d

-- Result
-- days_date   days_timestamp
-- 135         135.0
```

## Interval in weeks

```sql
SELECT
    -- Number of days divided by 7 and truncated
    TRUNC(DATE_PART('day', end_date - start_date)/7)
FROM d

-- Result
-- 19.0
```

## Interval in hours

```sql
SELECT
    -- Number of days multiplied by 24 hours
    DATE_PART('day', end_date - start_date) * 24
    -- Add hours difference
    + DATE_PART('hour', end_date - start_date)
FROM d

-- Result
-- 3243.0
```

## Interval in minutes

```sql
SELECT
    -- Number of days multiplied by 1440 minutes
    DATE_PART('day', end_date - start_date) * 24 * 60
    -- Add minutes difference
    + DATE_PART('minute', end_date - start_date)
FROM d

-- Result
-- 194428.0
```
