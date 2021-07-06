# Get today and yesterday date in Python

In Python, the [datetime](https://docs.python.org/fr/3/library/datetime.html) library lets you get the current date or datetime.

```python
# Import library
import datetime
```

## Get current date

```python
# Get date for today
datetime.date.today()
```

    datetime.date(2020, 11, 7)

```python
# Get datetime for now
datetime.datetime.now()
```

    datetime.datetime(2020, 11, 7, 5, 51, 10, 787948)

## Add or substract time from current date

```python
# Substract 1 day from today
datetime.date.today() - datetime.timedelta(1)
```

    datetime.date(2020, 11, 6)

```python
# Add 1 week to current datetime
datetime.datetime.now() + datetime.timedelta(weeks=1)
```

    datetime.datetime(2020, 11, 14, 5, 51, 10, 807394)

## Convert to string

To convert a date or datetime object to a string, simply use `strftime()`.

```python
# Convert yesterday date to a formatted string
yesterday = datetime.date.today() - datetime.timedelta(1)
yesterday.strftime("%Y-%m-%d")
```

    '2020-11-06'

