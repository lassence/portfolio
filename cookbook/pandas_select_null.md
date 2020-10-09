# Pandas DataFrames: select rows with NA values in any column


```python
# Import libraries
import pandas as pd
import numpy as np

# Create sample dataframe
df = pd.DataFrame({'population':[2148000, np.nan, 861635, 232741, np.nan], 
                  'area_km':[105.4, 47.87, 240.6, np.nan, 78.26]},
                  index=['Paris', 'Lyon',  'Marseille', 'Lille', 'Strasbourg'])
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
      <th>population</th>
      <th>area_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Paris</th>
      <td>2148000.0</td>
      <td>105.40</td>
    </tr>
    <tr>
      <th>Lyon</th>
      <td>NaN</td>
      <td>47.87</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>861635.0</td>
      <td>240.60</td>
    </tr>
    <tr>
      <th>Lille</th>
      <td>232741.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Strasbourg</th>
      <td>NaN</td>
      <td>78.26</td>
    </tr>
  </tbody>
</table>
</div>



## Select rows that have at least one NA value


```python
# Standard way
df[df.isnull().any(axis=1)]
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
      <th>population</th>
      <th>area_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Lyon</th>
      <td>NaN</td>
      <td>47.87</td>
    </tr>
    <tr>
      <th>Lille</th>
      <td>232741.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Strasbourg</th>
      <td>NaN</td>
      <td>78.26</td>
    </tr>
  </tbody>
</table>
</div>




```python
# With .loc and lambda (useful for method chaining)
df.loc[lambda x: x.isnull().any(axis=1)]
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
      <th>population</th>
      <th>area_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Lyon</th>
      <td>NaN</td>
      <td>47.87</td>
    </tr>
    <tr>
      <th>Lille</th>
      <td>232741.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>Strasbourg</th>
      <td>NaN</td>
      <td>78.26</td>
    </tr>
  </tbody>
</table>
</div>



## Filter out rows with NA values


```python
# Select rows that do not have any NA value
df.dropna()
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
      <th>population</th>
      <th>area_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Paris</th>
      <td>2148000.0</td>
      <td>105.4</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>861635.0</td>
      <td>240.6</td>
    </tr>
  </tbody>
</table>
</div>


