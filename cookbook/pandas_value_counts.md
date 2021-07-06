# Tips for pandas value_counts()

```python
# Import libraries
import numpy as np
import pandas as pd

# Generate random data
df = pd.DataFrame({'value': np.concatenate([[i]*np.random.randint(1,20) for i in range(10)])})
df.iloc[[3]] = np.nan
```

`value_counts()` is a very handy function, that groups together values of a Series or DataFrame, and returns their count. With a few arguments, you can expand its capabilities.

```python
# Default behaviour
df.value_counts()
```

    value
    3.0      17
    5.0      17
    2.0      16
    9.0      15
    6.0      13
    1.0      10
    7.0      10
    0.0       2
    4.0       2
    8.0       2
    dtype: int64

## Relative frequencies

To get the relative frequencies instead of the absolue count, use `normalize=True`. This is equivalent to dividing each row by the total:

```python
# Normalized count, i.e. relative frequency of values
df.value_counts(normalize=True)
```

    value
    3.0      0.163462
    5.0      0.163462
    2.0      0.153846
    9.0      0.144231
    6.0      0.125000
    1.0      0.096154
    7.0      0.096154
    0.0      0.019231
    4.0      0.019231
    8.0      0.019231
    dtype: float64

## Group into buckets

It is also possible to group values into buckets with `bins=True`, which is a quicker than calling `pd.cut`:

```python
# Group values into buckets -- only works with Series
df['value'].value_counts(bins=5)
```

    (1.8, 3.6]                      33
    (5.4, 7.2]                      23
    (3.6, 5.4]                      19
    (7.2, 9.0]                      17
    (-0.009999999999999998, 1.8]    12
    Name: value, dtype: int64

## Include NA values

By default, NA values are not counted. To include them, specify `dropna=False`:

```python
# Without NA
df.value_counts()
```

    value
    3.0      17
    5.0      17
    2.0      16
    9.0      15
    6.0      13
    1.0      10
    7.0      10
    0.0       2
    4.0       2
    8.0       2
    dtype: int64

```python
# Including NA -- only works for Series
df['value'].value_counts(dropna=False)
```

    3.0    17
    5.0    17
    2.0    16
    9.0    15
    6.0    13
    7.0    10
    1.0    10
    0.0     2
    4.0     2
    8.0     2
    NaN     1
    Name: value, dtype: int64

