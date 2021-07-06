# Options for DataFrame *info()*

When working with DataFrames, perhaps the most commonly used function to get information about your data is `info()`. This function has a [few parameters](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.info.html) that can be useful, particularily when working with large datasets.

```python
# Import libraries
import pandas as pd
```

```python
%%bigquery df
# Get large sample data
SELECT *
FROM `bigquery-public-data.hacker_news.stories`
```

## Without parameters

Printing information without any options will indicate a memory usage of 179MB. 
Also, note that it doesn't display the number of non-Null values for each column, because this dataset is too large.

```python
# Basic usage without parameters
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1959809 entries, 0 to 1959808
    Data columns (total 12 columns):
     #   Column       Dtype              
    ---  ------       -----              
     0   id           int64              
     1   by           object             
     2   score        float64            
     3   time         float64            
     4   time_ts      datetime64[ns, UTC]
     5   title        object             
     6   url          object             
     7   text         object             
     8   deleted      object             
     9   dead         object             
     10  descendants  float64            
     11  author       object             
    dtypes: datetime64[ns, UTC](1), float64(3), int64(1), object(7)
    memory usage: 179.4+ MB

## Real memory usage

Specifying `memory_usage='deep'` will enable deep memory introspection, and show real memory usage, which is often much higher than the standard estimation. In this example, it is five times higher than previously estimated.

```python
# Full memory usage
df.info(memory_usage='deep')
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1959809 entries, 0 to 1959808
    Data columns (total 12 columns):
     #   Column       Dtype              
    ---  ------       -----              
     0   id           int64              
     1   by           object             
     2   score        float64            
     3   time         float64            
     4   time_ts      datetime64[ns, UTC]
     5   title        object             
     6   url          object             
     7   text         object             
     8   deleted      object             
     9   dead         object             
     10  descendants  float64            
     11  author       object             
    dtypes: datetime64[ns, UTC](1), float64(3), int64(1), object(7)
    memory usage: 1007.3 MB

## Force count of Null values

On large datasets, counting Null values in each columns is deactivated, to avoid lengthy calculation. To force the display, set `show_counts=True`.

```python
# Force Null values counting
df.info(show_counts=True)
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1959809 entries, 0 to 1959808
    Data columns (total 12 columns):
     #   Column       Non-Null Count    Dtype              
    ---  ------       --------------    -----              
     0   id           1959809 non-null  int64              
     1   by           1841269 non-null  object             
     2   score        1841269 non-null  float64            
     3   time         1934088 non-null  float64            
     4   time_ts      1934088 non-null  datetime64[ns, UTC]
     5   title        1841267 non-null  object             
     6   url          1839757 non-null  object             
     7   text         1425167 non-null  object             
     8   deleted      92818 non-null    object             
     9   dead         394344 non-null   object             
     10  descendants  1741598 non-null  float64            
     11  author       1841269 non-null  object             
    dtypes: datetime64[ns, UTC](1), float64(3), int64(1), object(7)
    memory usage: 179.4+ MB

## Compact mode

If you don't want to display the full summary with details about each columns, use the compact mode with `verbose=False`.

```python
# Non verbose mode
df.info(verbose=False)
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1959809 entries, 0 to 1959808
    Columns: 12 entries, id to author
    dtypes: datetime64[ns, UTC](1), float64(3), int64(1), object(7)
    memory usage: 179.4+ MB

