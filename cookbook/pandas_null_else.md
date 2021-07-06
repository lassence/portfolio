# Pandas: use a column value if not Null, else an other column

When calculating a new column in a pandas DataFrame, if you want to use the value of column if it is not Null, or fall back on the value of another column, you can do it with a one-liner.

```python
# Import libraries
import pandas as pd
import numpy as np

# Create a sample DataFrame
df = pd.DataFrame(np.random.random(size=(10, 2)), columns=list('AB')).round(3)
df.iloc[[2,3,5,8], 0] = np.nan
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.591</td>
      <td>0.394</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.573</td>
      <td>0.374</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>0.309</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>0.254</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.231</td>
      <td>0.230</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td>0.099</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.392</td>
      <td>0.703</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.447</td>
      <td>0.496</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td>0.058</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.597</td>
      <td>0.658</td>
    </tr>
  </tbody>
</table>
</div>

Here is the code:

```python
# Create a third column, that will take column A value if not Null, or fall back on B
df['C'] = df['A'].fillna(df['B'])
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.591</td>
      <td>0.394</td>
      <td>0.591</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.573</td>
      <td>0.374</td>
      <td>0.573</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>0.309</td>
      <td>0.309</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>0.254</td>
      <td>0.254</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.231</td>
      <td>0.230</td>
      <td>0.231</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td>0.099</td>
      <td>0.099</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.392</td>
      <td>0.703</td>
      <td>0.392</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.447</td>
      <td>0.496</td>
      <td>0.447</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td>0.058</td>
      <td>0.058</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.597</td>
      <td>0.658</td>
      <td>0.597</td>
    </tr>
  </tbody>
</table>
</div>

You can even chain it, to get a third column value, if the first two columns are Null:

```python
# Add some data
df['C'] = np.random.random(size=(10, 1)).round(3)
df.iloc[[1,4,5,8], 1] = np.nan

# Create a fourth column, that would take column C value if the first two are Null
df['D'] = df['A'].fillna(df['B']).fillna(df['C'])
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.591</td>
      <td>0.394</td>
      <td>0.637</td>
      <td>0.591</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.573</td>
      <td>NaN</td>
      <td>0.331</td>
      <td>0.573</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>0.309</td>
      <td>0.738</td>
      <td>0.309</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>0.254</td>
      <td>0.856</td>
      <td>0.254</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.231</td>
      <td>NaN</td>
      <td>0.160</td>
      <td>0.231</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.926</td>
      <td>0.926</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.392</td>
      <td>0.703</td>
      <td>0.847</td>
      <td>0.392</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.447</td>
      <td>0.496</td>
      <td>0.824</td>
      <td>0.447</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.529</td>
      <td>0.529</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.597</td>
      <td>0.658</td>
      <td>0.948</td>
      <td>0.597</td>
    </tr>
  </tbody>
</table>
</div>

