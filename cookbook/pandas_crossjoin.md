# Cross-join two pandas DataFrame

Say you have groups and subgroups, and you want to combine in a DataFrame all possible combinations of groups and subgroups.

```python
# Import libraries
import pandas as pd
from IPython.display import display

# Create DataFrames
df_groups = pd.DataFrame({'group': ['A', 'B', 'C']})
display(df_groups)

df_subgroups = pd.DataFrame({'subgroup': list(range(5))})
display(df_subgroups)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>subgroup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>

This can be done with a cross-join, using the `merge()` function with argument `how='cross'`.

```python
# Combine DataFrames with a cross-join
df_groups.merge(df_subgroups, how='cross')
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>subgroup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>B</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>B</td>
      <td>2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>B</td>
      <td>3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>B</td>
      <td>4</td>
    </tr>
    <tr>
      <th>10</th>
      <td>C</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>C</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>C</td>
      <td>2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>C</td>
      <td>3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>C</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>

