# Pivot pandas Dataframes with non-numeric values

## Setup


```python
# Import libraries
import pandas as pd
import numpy as np

# Sample DataFrame
df = pd.DataFrame({
    'advertiser':['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
    'keyword': ['screen', 'phone', 'laptop', 'keyboard', 'phone', 'tablet', 'flat', 'screen', 'phone', 'computer'],
    'clicks': np.random.randint(low=20, high=50, size=10)
})
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>advertiser</th>
      <th>keyword</th>
      <th>clicks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alice</td>
      <td>screen</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Alice</td>
      <td>phone</td>
      <td>46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Alice</td>
      <td>laptop</td>
      <td>34</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>keyboard</td>
      <td>36</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Bob</td>
      <td>phone</td>
      <td>24</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Bob</td>
      <td>tablet</td>
      <td>33</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Bob</td>
      <td>flat</td>
      <td>25</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Charlie</td>
      <td>screen</td>
      <td>35</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Charlie</td>
      <td>phone</td>
      <td>25</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Charlie</td>
      <td>computer</td>
      <td>35</td>
    </tr>
  </tbody>
</table>
</div>



## Pivot keywords to columns


```python
# Pivot keywords to columns
(
    df
    .pivot(index='advertiser', columns='keyword', values='clicks')
)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>keyword</th>
      <th>computer</th>
      <th>flat</th>
      <th>keyboard</th>
      <th>laptop</th>
      <th>phone</th>
      <th>screen</th>
      <th>tablet</th>
    </tr>
    <tr>
      <th>advertiser</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Alice</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>36.0</td>
      <td>34.0</td>
      <td>46.0</td>
      <td>34.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Bob</th>
      <td>NaN</td>
      <td>25.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>24.0</td>
      <td>NaN</td>
      <td>33.0</td>
    </tr>
    <tr>
      <th>Charlie</th>
      <td>35.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>25.0</td>
      <td>35.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Pivot keywords to columns, ranked by clicks
(
    df
    .sort_values('clicks', ascending=False)
    .groupby('advertiser')
    .agg(list)
    .apply(lambda x: pd.Series(x['keyword']), axis=1)
)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
    <tr>
      <th>advertiser</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Alice</th>
      <td>phone</td>
      <td>keyboard</td>
      <td>screen</td>
      <td>laptop</td>
    </tr>
    <tr>
      <th>Bob</th>
      <td>tablet</td>
      <td>flat</td>
      <td>phone</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Charlie</th>
      <td>screen</td>
      <td>computer</td>
      <td>phone</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>


