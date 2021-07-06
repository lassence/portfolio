# Flatten multi-index columns in DataFrames

## Setup

```python
# Import libraries
import pandas as pd
import seaborn as sns

# Load sample data in a DataFrame
df = (
    sns.load_dataset('iris')
    [['species', 'petal_length']]
    .groupby('species')
    .agg(['min', 'mean', 'max'])
)
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">petal_length</th>
    </tr>
    <tr>
      <th></th>
      <th>min</th>
      <th>mean</th>
      <th>max</th>
    </tr>
    <tr>
      <th>species</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>setosa</th>
      <td>1.0</td>
      <td>1.462</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>versicolor</th>
      <td>3.0</td>
      <td>4.260</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>virginica</th>
      <td>4.5</td>
      <td>5.552</td>
      <td>6.9</td>
    </tr>
  </tbody>
</table>
</div>

## Drop a level

```python
# Just drop the first level
df.droplevel(0, axis=1)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>min</th>
      <th>mean</th>
      <th>max</th>
    </tr>
    <tr>
      <th>species</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>setosa</th>
      <td>1.0</td>
      <td>1.462</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>versicolor</th>
      <td>3.0</td>
      <td>4.260</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>virginica</th>
      <td>4.5</td>
      <td>5.552</td>
      <td>6.9</td>
    </tr>
  </tbody>
</table>
</div>

## Concatenate names

```python
# Method chaining
df.set_axis(['_'.join(col).strip() for col in df.columns.values], axis=1)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>petal_length_min</th>
      <th>petal_length_mean</th>
      <th>petal_length_max</th>
    </tr>
    <tr>
      <th>species</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>setosa</th>
      <td>1.0</td>
      <td>1.462</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>versicolor</th>
      <td>3.0</td>
      <td>4.260</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>virginica</th>
      <td>4.5</td>
      <td>5.552</td>
      <td>6.9</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Classic way
df.columns = ['_'.join(col).strip() for col in df.columns.values]
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>petal_length_min</th>
      <th>petal_length_mean</th>
      <th>petal_length_max</th>
    </tr>
    <tr>
      <th>species</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>setosa</th>
      <td>1.0</td>
      <td>1.462</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>versicolor</th>
      <td>3.0</td>
      <td>4.260</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>virginica</th>
      <td>4.5</td>
      <td>5.552</td>
      <td>6.9</td>
    </tr>
  </tbody>
</table>
</div>
