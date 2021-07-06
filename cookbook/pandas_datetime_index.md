# Date indexes in pandas DataFrames

Pandas provides convenient features to select, slice and aggregate DataFrames that have date or datetime indexes.

## Setup

```python
# Import libraries
import pandas as pd
```

```python
# Read sample data with date index
df = pd.read_csv('data/finance_data.csv', parse_dates=['Date'])
df = df.set_index('Date').loc[lambda x: x['Name'] == 'Nasdaq100', ['Value']]
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-02</th>
      <td>6360.87</td>
    </tr>
    <tr>
      <th>2019-01-03</th>
      <td>6147.13</td>
    </tr>
    <tr>
      <th>2019-01-04</th>
      <td>6422.67</td>
    </tr>
    <tr>
      <th>2019-01-07</th>
      <td>6488.25</td>
    </tr>
    <tr>
      <th>2019-01-08</th>
      <td>6551.85</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-05-04</th>
      <td>8834.11</td>
    </tr>
    <tr>
      <th>2020-05-05</th>
      <td>8930.62</td>
    </tr>
    <tr>
      <th>2020-05-06</th>
      <td>8984.86</td>
    </tr>
    <tr>
      <th>2020-05-07</th>
      <td>9101.88</td>
    </tr>
    <tr>
      <th>2020-05-08</th>
      <td>9220.35</td>
    </tr>
  </tbody>
</table>
<p>341 rows × 1 columns</p>
</div>

## Select dates in DataFrames

With a date index, you can easily select a specific year, month or day.

```python
# Select year
df['2020']
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-01-02</th>
      <td>8872.22</td>
    </tr>
    <tr>
      <th>2020-01-03</th>
      <td>8793.90</td>
    </tr>
    <tr>
      <th>2020-01-06</th>
      <td>8848.52</td>
    </tr>
    <tr>
      <th>2020-01-07</th>
      <td>8846.45</td>
    </tr>
    <tr>
      <th>2020-01-08</th>
      <td>8912.37</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-05-04</th>
      <td>8834.11</td>
    </tr>
    <tr>
      <th>2020-05-05</th>
      <td>8930.62</td>
    </tr>
    <tr>
      <th>2020-05-06</th>
      <td>8984.86</td>
    </tr>
    <tr>
      <th>2020-05-07</th>
      <td>9101.88</td>
    </tr>
    <tr>
      <th>2020-05-08</th>
      <td>9220.35</td>
    </tr>
  </tbody>
</table>
<p>89 rows × 1 columns</p>
</div>

```python
# Select month
df['2020-05']
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-05-01</th>
      <td>8718.18</td>
    </tr>
    <tr>
      <th>2020-05-04</th>
      <td>8834.11</td>
    </tr>
    <tr>
      <th>2020-05-05</th>
      <td>8930.62</td>
    </tr>
    <tr>
      <th>2020-05-06</th>
      <td>8984.86</td>
    </tr>
    <tr>
      <th>2020-05-07</th>
      <td>9101.88</td>
    </tr>
    <tr>
      <th>2020-05-08</th>
      <td>9220.35</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Select period interval
df['2020-02-01':'2020-02-10']
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-02-03</th>
      <td>9126.23</td>
    </tr>
    <tr>
      <th>2020-02-04</th>
      <td>9334.06</td>
    </tr>
    <tr>
      <th>2020-02-05</th>
      <td>9367.48</td>
    </tr>
    <tr>
      <th>2020-02-06</th>
      <td>9445.92</td>
    </tr>
    <tr>
      <th>2020-02-07</th>
      <td>9401.10</td>
    </tr>
    <tr>
      <th>2020-02-10</th>
      <td>9516.84</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Select period after or before a date
df['2020-04-30':]
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-30</th>
      <td>9000.51</td>
    </tr>
    <tr>
      <th>2020-05-01</th>
      <td>8718.18</td>
    </tr>
    <tr>
      <th>2020-05-04</th>
      <td>8834.11</td>
    </tr>
    <tr>
      <th>2020-05-05</th>
      <td>8930.62</td>
    </tr>
    <tr>
      <th>2020-05-06</th>
      <td>8984.86</td>
    </tr>
    <tr>
      <th>2020-05-07</th>
      <td>9101.88</td>
    </tr>
    <tr>
      <th>2020-05-08</th>
      <td>9220.35</td>
    </tr>
  </tbody>
</table>
</div>

## Aggregate rows

It is also trivial to apply aggregation at a time level, like month or week for example, and compute metrics with `resample()`.

```python
# Number of data points per month
df['2020'].resample('M').count()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-01-31</th>
      <td>21</td>
    </tr>
    <tr>
      <th>2020-02-29</th>
      <td>19</td>
    </tr>
    <tr>
      <th>2020-03-31</th>
      <td>22</td>
    </tr>
    <tr>
      <th>2020-04-30</th>
      <td>21</td>
    </tr>
    <tr>
      <th>2020-05-31</th>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Mean value per week
df['2020-04'].resample('W').mean()
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-05</th>
      <td>7550.0200</td>
    </tr>
    <tr>
      <th>2020-04-12</th>
      <td>8149.7600</td>
    </tr>
    <tr>
      <th>2020-04-19</th>
      <td>8641.4200</td>
    </tr>
    <tr>
      <th>2020-04-26</th>
      <td>8644.4500</td>
    </tr>
    <tr>
      <th>2020-05-03</th>
      <td>8874.6325</td>
    </tr>
  </tbody>
</table>
</div>

