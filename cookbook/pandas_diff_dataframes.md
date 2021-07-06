# Pandas: diff two DataFrames

```python
# Import libraries
import pandas as pd
import numpy as np 

# Create sample dataframes
df1 = pd.DataFrame({'city': ['Paris', 'Lyon',  'Marseille', 'Lille', 'Strasbourg'],
                    'population': [2148000, 513300, 861635, 232741, 277270]})
df2 = df1.copy()
df2.iloc[1,1] = 0

df2
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>population</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Paris</td>
      <td>2148000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lyon</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Marseille</td>
      <td>861635</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Lille</td>
      <td>232741</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Strasbourg</td>
      <td>277270</td>
    </tr>
  </tbody>
</table>
</div>

## Check if DataFrames are identical

```python
# Check if dataframes are identical
df1.equals(df2)
```

    False

## Get delta rows between DataFrames

```python
# Get rows that are different between dataframes, with `drop_duplicates()`
pd.concat([df1,df2]).drop_duplicates(keep=False)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>population</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Lyon</td>
      <td>513300</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lyon</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Get delta rows with `merge()`
df1.merge(df2, how='outer', indicator=True).loc[lambda x: x['_merge'] != "both"]
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>population</th>
      <th>_merge</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Lyon</td>
      <td>513300</td>
      <td>left_only</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Lyon</td>
      <td>0</td>
      <td>right_only</td>
    </tr>
  </tbody>
</table>
</div>

## Get common rows between DataFrames

```python
# Get common rows between dataframes
df1.merge(df2, how='inner')
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>population</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Paris</td>
      <td>2148000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Marseille</td>
      <td>861635</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Lille</td>
      <td>232741</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Strasbourg</td>
      <td>277270</td>
    </tr>
  </tbody>
</table>
</div>

