# Handle infinity values

```python
# Import libraries
import pandas as pd
import numpy as np
from numpy.random import randint

# Create sample dataframe
df = (
    pd.DataFrame({'clicks': randint(1, 20, 5), 
                  'impressions': list(randint(1000, 3000, 4)) + [0]})
    .assign(ctr=lambda x: x['clicks']/x['impressions'])
)
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>clicks</th>
      <th>impressions</th>
      <th>ctr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>2850</td>
      <td>0.002456</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11</td>
      <td>1896</td>
      <td>0.005802</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>1457</td>
      <td>0.006177</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9</td>
      <td>1698</td>
      <td>0.005300</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>0</td>
      <td>inf</td>
    </tr>
  </tbody>
</table>
</div>

In some cases where a float is divided by zero, you may encounter infinity values, negative or positive: `np.inf` or `-np.inf`.

## Replace infinity values

To replace those infinity values, you can use `replace()`:

```python
# Replace infinity with 0
df.replace([np.inf, -np.inf], 0)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>clicks</th>
      <th>impressions</th>
      <th>ctr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>2850</td>
      <td>0.002456</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11</td>
      <td>1896</td>
      <td>0.005802</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>1457</td>
      <td>0.006177</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9</td>
      <td>1698</td>
      <td>0.005300</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>0</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>

## Drop rows

If you want to drop the rows, replace infinity values with NaN and follow with `dropna()`:

```python
# Replace with NaN and drop rows
df.replace([np.inf, -np.inf], np.nan).dropna()
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>clicks</th>
      <th>impressions</th>
      <th>ctr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>2850</td>
      <td>0.002456</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11</td>
      <td>1896</td>
      <td>0.005802</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9</td>
      <td>1457</td>
      <td>0.006177</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9</td>
      <td>1698</td>
      <td>0.005300</td>
    </tr>
  </tbody>
</table>
</div>

