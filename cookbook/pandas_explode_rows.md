# Pandas DataFrames: explode and regroup lists into rows

## Setup

```python
# Import libraries
import pandas as pd

# Create sample dataframe
df = pd.DataFrame({'zip_codes':["75002, 75005, 75007, 75019, 75020", "13000, 13001, 13005", "69001, 69003, 69004"]}, 
                  index=['Paris', 'Marseille', 'Lyon'])
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>zip_codes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Paris</th>
      <td>75002, 75005, 75007, 75019, 75020</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>13000, 13001, 13005</td>
    </tr>
    <tr>
      <th>Lyon</th>
      <td>69001, 69003, 69004</td>
    </tr>
  </tbody>
</table>
</div>

## Split values and expand into multiple rows

Use `explode()` to break down a list into multiple rows

```python
# Split values on commas, and expand into multiple rows
df = (
    df
    .assign(zip_codes=lambda x: x['zip_codes'].str.split(','))
    .explode('zip_codes')
)
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>zip_codes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Paris</th>
      <td>75002</td>
    </tr>
    <tr>
      <th>Paris</th>
      <td>75005</td>
    </tr>
    <tr>
      <th>Paris</th>
      <td>75007</td>
    </tr>
    <tr>
      <th>Paris</th>
      <td>75019</td>
    </tr>
    <tr>
      <th>Paris</th>
      <td>75020</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>13000</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>13001</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>13005</td>
    </tr>
    <tr>
      <th>Lyon</th>
      <td>69001</td>
    </tr>
    <tr>
      <th>Lyon</th>
      <td>69003</td>
    </tr>
    <tr>
      <th>Lyon</th>
      <td>69004</td>
    </tr>
  </tbody>
</table>
</div>

## Regroup rows into a list 

The inverse operation, regrouping multiple rows into a list, is achieved with a `grouby()` followed by `agg(list)`.

```python
# Regroup rows with the same index into a list
(
    df
    .groupby(df.index)
    .agg(list)
)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>zip_codes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Lyon</th>
      <td>[69001,  69003,  69004]</td>
    </tr>
    <tr>
      <th>Marseille</th>
      <td>[13000,  13001,  13005]</td>
    </tr>
    <tr>
      <th>Paris</th>
      <td>[75002,  75005,  75007,  75019,  75020]</td>
    </tr>
  </tbody>
</table>
</div>

