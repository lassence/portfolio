# Handling dates with pandas

## Convert strings to datetime

```python
import pandas as pd

# Create a dataframe with dates 
df = pd.DataFrame(['01-01-2020', '01-02-2020', '01-03-2020', '01-04-2020', '01-05-2020'], columns=['date'])
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>01-01-2020</td>
    </tr>
    <tr>
      <th>1</th>
      <td>01-02-2020</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01-03-2020</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01-04-2020</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01-05-2020</td>
    </tr>
  </tbody>
</table>
</div>

`pd.to_datetime()` is the most useful pandas function for converting strings to datetime. It tries to guess the date format if you don't specify it. For a cheatsheet on Python's *strftime* parameters, you can refer to [strftime.org](https://strftime.org/).

```python
# Without specifying a date format
pd.to_datetime(df['date'])
```

    0   2020-01-01
    1   2020-01-02
    2   2020-01-03
    3   2020-01-04
    4   2020-01-05
    Name: date, dtype: datetime64[ns]

```python
# With the format specified
df['date_converted'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
df['date_converted']
```

    0   2020-01-01
    1   2020-02-01
    2   2020-03-01
    3   2020-04-01
    4   2020-05-01
    Name: date_converted, dtype: datetime64[ns]

## Extract date parts

The `pd.Series.dt` accessor extracts parts of a timestamp.

```python
# Extract year
df['date_converted'].dt.year
```

    0    2020
    1    2020
    2    2020
    3    2020
    4    2020
    Name: date_converted, dtype: int64

```python
# Extract week day
df['date_converted'].dt.weekday
```

    0    2
    1    5
    2    6
    3    2
    4    4
    Name: date_converted, dtype: int64

## Truncate date

To truncate a date or datetime to a less granular frequency, use `dt.to_period()` with a specified [offset](https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases), for example:  

* `D`: calendar day
* `W`: week
* `M`: month
* `Q`: quarter
* `Y`: year

```python
# Truncate date to month
df['date_converted'].dt.to_period('M')
```

    0    2020-01
    1    2020-02
    2    2020-03
    3    2020-04
    4    2020-05
    Name: date_converted, dtype: period[M]

```python
# Truncate date to quarter
df['date_converted'].dt.to_period('Q')
```

    0    2020Q1
    1    2020Q1
    2    2020Q1
    3    2020Q2
    4    2020Q2
    Name: date_converted, dtype: period[Q-DEC]

## Convert date to string

`strftime()` is the Python function for converting datetime to strings. You can apply it to a Series or DataFrame with `apply()`.

```python
# Convert to string, with a different format
df['date_converted'].apply(lambda x: x.strftime('%B %-d, %Y'))
```

    0     January 1, 2020
    1    February 1, 2020
    2       March 1, 2020
    3       April 1, 2020
    4         May 1, 2020
    Name: date_converted, dtype: object

## Convert epoch to date

`pd.to_datetime()` can convert an UNIX epoch up to the nanosecond, specified with the *unit* parameter.

```python
# Convert epoch in seconds to date
pd.to_datetime(1587239920, unit='s')
```

    Timestamp('2020-04-18 19:58:40')

