# Rearrange layers with Matplotlib and Seaborn plots

## Setup

```python
# Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()
```

```python
%%bigquery df
# Get NYC temperatures as sample data
SELECT
    year,
    mo AS month,
    AVG(temp) AS temp
FROM `bigquery-public-data.noaa_gsod.gsod*` 
WHERE 
    wban = '94728'
    AND CAST(mo AS INT64) <= 6
GROUP BY year, mo
ORDER BY year, mo
```

```python
# Compute quartiles for each month
quartiles = (
    df
    .groupby('month')
    .quantile([.25, .75])
    .reset_index()
    .pivot(index='month', columns='level_1')
    .set_axis(['low', 'high'], axis=1)
)
quartiles
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>low</th>
      <th>high</th>
    </tr>
    <tr>
      <th>month</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>01</th>
      <td>28.928226</td>
      <td>35.102419</td>
    </tr>
    <tr>
      <th>02</th>
      <td>32.170536</td>
      <td>37.488793</td>
    </tr>
    <tr>
      <th>03</th>
      <td>39.147581</td>
      <td>42.965323</td>
    </tr>
    <tr>
      <th>04</th>
      <td>50.396667</td>
      <td>54.156667</td>
    </tr>
    <tr>
      <th>05</th>
      <td>60.135484</td>
      <td>64.251613</td>
    </tr>
    <tr>
      <th>06</th>
      <td>69.716667</td>
      <td>72.186667</td>
    </tr>
  </tbody>
</table>
</div>

## Reorder plot layers with z-order

In some cases, multiple plots over the same figure can be arranged in an unwanted order, that do not follow the sequence of the code.  
To rearrange the layers order, you can specify their z-index with `zorder`:

```python
# Plot with default layers z-order
fig, ax = plt.subplots(1,2, figsize=(14,6))
sns.lineplot(data=df, x='month', y='temp', units='year', estimator=None, color='grey', alpha=.5, ax=ax[0])
ax[0].fill_between(x=quartiles.index, y1=quartiles['low'], y2=quartiles['high'], alpha=.5)
ax[0].set_title("Without z-order")

# Specify z-order
sns.lineplot(data=df, x='month', y='temp', units='year', estimator=None, color='grey', alpha=.5, ax=ax[1], zorder=1)
ax[1].fill_between(x=quartiles.index, y1=quartiles['low'], y2=quartiles['high'], alpha=.5, zorder=2)
ax[1].set_title("With z-order specified");
```

    
![png](python_plot_zorder_files/python_plot_zorder_7_0.png)
    

