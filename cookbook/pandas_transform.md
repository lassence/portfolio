# Pandas: apply computation within groups in a DataFrame

One useful capability of pandas is to execute computations within groups of a DataFrame. This is achieved using `groupby()` followed by `transform()`.

```python
# Import libraries
import pandas as pd
import seaborn as sns

# Load sample data in a DataFrame
df = (
    sns.load_dataset('iris')
    .sample(n=12, random_state=24)
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
      <td>3.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.8</td>
    </tr>
    <tr>
      <th>5</th>
      <td>versicolor</td>
      <td>2.4</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>8</th>
      <td>virginica</td>
      <td>2.9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>virginica</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>10</th>
      <td>virginica</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>virginica</td>
      <td>3.4</td>
    </tr>
  </tbody>
</table>
</div>

## Compute mean at group-level

To get group-level statistics like mean, sum or count, use `transform('function')`.

```python
# Get group mean
df.assign(mean=
    df.groupby('species').transform('mean')
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
      <th>mean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.4</td>
      <td>3.440000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.7</td>
      <td>3.440000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.2</td>
      <td>3.440000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.1</td>
      <td>3.440000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.8</td>
      <td>3.440000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>versicolor</td>
      <td>2.4</td>
      <td>2.533333</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
      <td>2.533333</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.5</td>
      <td>2.533333</td>
    </tr>
    <tr>
      <th>8</th>
      <td>virginica</td>
      <td>2.9</td>
      <td>3.025000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>virginica</td>
      <td>2.8</td>
      <td>3.025000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>virginica</td>
      <td>3.0</td>
      <td>3.025000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>virginica</td>
      <td>3.4</td>
      <td>3.025000</td>
    </tr>
  </tbody>
</table>
</div>

## Standardize values

You can center values inside a group by substracting the group mean to each row.

```python
# Standardize values
df.assign(standardized=
    df.groupby('species').transform(lambda x: x - x.mean())
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
      <th>standardized</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.4</td>
      <td>-0.040000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.7</td>
      <td>0.260000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.2</td>
      <td>-0.240000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.1</td>
      <td>-0.340000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.8</td>
      <td>0.360000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>versicolor</td>
      <td>2.4</td>
      <td>-0.133333</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
      <td>0.166667</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.5</td>
      <td>-0.033333</td>
    </tr>
    <tr>
      <th>8</th>
      <td>virginica</td>
      <td>2.9</td>
      <td>-0.125000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>virginica</td>
      <td>2.8</td>
      <td>-0.225000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>virginica</td>
      <td>3.0</td>
      <td>-0.025000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>virginica</td>
      <td>3.4</td>
      <td>0.375000</td>
    </tr>
  </tbody>
</table>
</div>

## Rank values inside groups

Besides computing group-wise values, you can also rank values within each group.

```python
# Rank values
df.assign(rank=
    df.groupby('species').transform(lambda x: x.rank())
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
      <th>rank</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.7</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.2</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.1</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.8</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>versicolor</td>
      <td>2.4</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.5</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>virginica</td>
      <td>2.9</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>virginica</td>
      <td>2.8</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>virginica</td>
      <td>3.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>virginica</td>
      <td>3.4</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
</div>

## Error when output has multiple columns

If the result of the transform generates more than 1 column, and you try to assign it to a column of an existing DataFrame, you will encounter an error like `ValueError: Wrong number of items passed X, placement implies 1`. To avoid this, pass only one column in the result:

```python
df.assign(rank=
    df.groupby('species').transform(lambda x: x.rank()).iloc[:, 0]
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>species</th>
      <th>sepal_width</th>
      <th>rank</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>setosa</td>
      <td>3.4</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>setosa</td>
      <td>3.7</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>setosa</td>
      <td>3.2</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>setosa</td>
      <td>3.1</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>setosa</td>
      <td>3.8</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>versicolor</td>
      <td>2.4</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>versicolor</td>
      <td>2.7</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>versicolor</td>
      <td>2.5</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>virginica</td>
      <td>2.9</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>virginica</td>
      <td>2.8</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>virginica</td>
      <td>3.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>virginica</td>
      <td>3.4</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
</div>

