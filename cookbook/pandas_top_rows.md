# Pandas: get top N rows of groups in a DataFrame

```python
# Import libraries
import pandas as pd
import seaborn as sns

# Load sample data in a DataFrame
df = (
    sns.load_dataset('iris')
    .sample(n=20, random_state=20)
    .sort_values('species')
    .reset_index(drop=True)
    [['species', 'sepal_width']]
)
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>setosa</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>versicolor</td>
      <td>2.9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>versicolor</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>10</th>
      <td>versicolor</td>
      <td>2.9</td>
    </tr>
    <tr>
      <th>11</th>
      <td>versicolor</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>12</th>
      <td>versicolor</td>
      <td>2.4</td>
    </tr>
    <tr>
      <th>13</th>
      <td>virginica</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>virginica</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>15</th>
      <td>virginica</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>16</th>
      <td>virginica</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>virginica</td>
      <td>2.2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>virginica</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>virginica</td>
      <td>2.8</td>
    </tr>
  </tbody>
</table>
</div>

## Get top N rows of each group

An option is to sort values, then use `groupby()` followed by `head()`

```python
# Get top 3 rows for each group, sorted by decreasing sepal width
(
    df
    .sort_values(['species', 'sepal_width'], ascending=[True, False])
    .groupby('species')
    .head(3)
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.4</td>
    </tr>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>versicolor</td>
      <td>2.9</td>
    </tr>
    <tr>
      <th>10</th>
      <td>versicolor</td>
      <td>2.9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>13</th>
      <td>virginica</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>virginica</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>virginica</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
</div>

