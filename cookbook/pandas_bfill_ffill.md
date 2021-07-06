# Forward or back-fill NA values in DataFrames

Back-filling replaces NaN with the next non-NA value, while forward-filling takes the previous non-NA value.
In pandas, this can be be done with `fillna(method=bfill|ffill)` or with the shortcuts `bfill()` and `ffill()`

```python
# Import libraries
import pandas as pd
import numpy as np
from numpy.random import randint

# Set seed
np.random.seed(21)

# Create sample data
df = (
    pd.DataFrame({'group': list('ABCDE'), 
                  'value': [randint(1000, 20000, randint(2, 5)) for i in range(5)]})
    .explode('value')
    .reset_index(drop=True)
)
df.loc[df.sample(frac=0.5).index, 'value'] = np.nan
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>6327</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>13898</td>
    </tr>
    <tr>
      <th>5</th>
      <td>C</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>18224</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>2646</td>
    </tr>
    <tr>
      <th>8</th>
      <td>D</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>D</td>
      <td>16613</td>
    </tr>
    <tr>
      <th>10</th>
      <td>E</td>
      <td>17118</td>
    </tr>
    <tr>
      <th>11</th>
      <td>E</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>E</td>
      <td>3352</td>
    </tr>
  </tbody>
</table>
</div>

## Back-fill and forward-fill 

```python
# Back-fill and forward-fill
(
    df
    .assign(value_bfill=df['value'].bfill(),
            value_ffill=df['value'].ffill())
)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>value</th>
      <th>value_bfill</th>
      <th>value_ffill</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>6327</td>
      <td>6327</td>
      <td>6327</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>NaN</td>
      <td>13898</td>
      <td>6327</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>NaN</td>
      <td>13898</td>
      <td>6327</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>NaN</td>
      <td>13898</td>
      <td>6327</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>13898</td>
      <td>13898</td>
      <td>13898</td>
    </tr>
    <tr>
      <th>5</th>
      <td>C</td>
      <td>NaN</td>
      <td>18224</td>
      <td>13898</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>18224</td>
      <td>18224</td>
      <td>18224</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>2646</td>
      <td>2646</td>
      <td>2646</td>
    </tr>
    <tr>
      <th>8</th>
      <td>D</td>
      <td>NaN</td>
      <td>16613</td>
      <td>2646</td>
    </tr>
    <tr>
      <th>9</th>
      <td>D</td>
      <td>16613</td>
      <td>16613</td>
      <td>16613</td>
    </tr>
    <tr>
      <th>10</th>
      <td>E</td>
      <td>17118</td>
      <td>17118</td>
      <td>17118</td>
    </tr>
    <tr>
      <th>11</th>
      <td>E</td>
      <td>NaN</td>
      <td>3352</td>
      <td>17118</td>
    </tr>
    <tr>
      <th>12</th>
      <td>E</td>
      <td>3352</td>
      <td>3352</td>
      <td>3352</td>
    </tr>
  </tbody>
</table>
</div>

## Forward- or back-fill within groups

```python
# Backfill and foward-fill within each group
(
    df
    .assign(value_bfill=df.groupby('group').transform(lambda x: x.bfill()),    # Back-fill
            value_ffill=df.groupby('group').transform(lambda x: x.ffill()),    # Forward-fill
            value_filled=lambda x: x['value_bfill'].fillna(x['value_ffill']))  # Get back- or forward-filled value
)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group</th>
      <th>value</th>
      <th>value_bfill</th>
      <th>value_ffill</th>
      <th>value_filled</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>6327</td>
      <td>6327.0</td>
      <td>6327.0</td>
      <td>6327.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6327.0</td>
      <td>6327.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6327.0</td>
      <td>6327.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>NaN</td>
      <td>13898.0</td>
      <td>NaN</td>
      <td>13898.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>13898</td>
      <td>13898.0</td>
      <td>13898.0</td>
      <td>13898.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>C</td>
      <td>NaN</td>
      <td>18224.0</td>
      <td>NaN</td>
      <td>18224.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>18224</td>
      <td>18224.0</td>
      <td>18224.0</td>
      <td>18224.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>2646</td>
      <td>2646.0</td>
      <td>2646.0</td>
      <td>2646.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>D</td>
      <td>NaN</td>
      <td>16613.0</td>
      <td>NaN</td>
      <td>16613.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>D</td>
      <td>16613</td>
      <td>16613.0</td>
      <td>16613.0</td>
      <td>16613.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>E</td>
      <td>17118</td>
      <td>17118.0</td>
      <td>17118.0</td>
      <td>17118.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>E</td>
      <td>NaN</td>
      <td>3352.0</td>
      <td>17118.0</td>
      <td>3352.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>E</td>
      <td>3352</td>
      <td>3352.0</td>
      <td>3352.0</td>
      <td>3352.0</td>
    </tr>
  </tbody>
</table>
</div>

