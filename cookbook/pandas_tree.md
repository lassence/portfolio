# Going up a tree with pandas

A common way of storing hierarchical data is the tree:

![tree structure](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Tree_%28computer_science%29.svg/258px-Tree_%28computer_science%29.svg.png)

In SQL, the methods for going up a tree are very different between SQL dialects. In pandas however, it is relatively simple.

For this example, we'll use the list of [Google Ads geotargets](https://developers.google.com/adwords/api/docs/appendix/geotargeting), that stores locations in a hierarchical structure, and get the list of all parents for each location.

## Setup

```python
# Import libraries
import pandas as pd
import numpy as np
```

```python
# Import Google Ads location data
df = (
    pd.read_csv('https://developers.google.com/adwords/api/docs/appendix/geo/geotargets-2021-02-24.csv')
    .rename(columns=lambda x: x.lower().replace(' ', '_'))
    .loc[lambda x: x['country_code'] == 'FR']
    .reset_index(drop=True)
    .assign(parent_id=lambda x: x['parent_id'].fillna(0).astype('int'))
    [['criteria_id', 'canonical_name', 'parent_id']]
)
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>criteria_id</th>
      <th>canonical_name</th>
      <th>parent_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1005781</td>
      <td>Algolsheim,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1005782</td>
      <td>Cernay,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1005783</td>
      <td>Colmar,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1005784</td>
      <td>Ensisheim,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1005785</td>
      <td>Erstein,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3755</th>
      <td>9060754</td>
      <td>Petite-France,Grand Est,France</td>
      <td>9068896</td>
    </tr>
    <tr>
      <th>3756</th>
      <td>9072487</td>
      <td>Les Halles,Ile-de-France,France</td>
      <td>20321</td>
    </tr>
    <tr>
      <th>3757</th>
      <td>9072488</td>
      <td>Place Vendome,Ile-de-France,France</td>
      <td>20321</td>
    </tr>
    <tr>
      <th>3758</th>
      <td>9072489</td>
      <td>Sorbonne,Ile-de-France,France</td>
      <td>20321</td>
    </tr>
    <tr>
      <th>3759</th>
      <td>9072490</td>
      <td>Saint-Germain-des-Pres,Ile-de-France,France</td>
      <td>20321</td>
    </tr>
  </tbody>
</table>
<p>3760 rows × 3 columns</p>
</div>

## Recursive function

```python
# Recursive algorithm: list the next parent if any, otherwise exit
def recursive(row, parents):
    if row['parent_id'] == 0:
        return parents
    else:
        parents.append(row['parent_id'])
        return recursive(df.loc[df['criteria_id'] == row['parent_id'], :].squeeze(), parents)

# Call the recursive function for each row
def get_parents(row):
    parents = []
    return recursive(row, parents)

# Apply the function and create a column with the parents list for each location
df['parents_list'] = df.apply(get_parents, axis=1)
```

```python
# Display resulting DataFrame
df.sort_values('parents_list')
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>criteria_id</th>
      <th>canonical_name</th>
      <th>parent_id</th>
      <th>parents_list</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>683</th>
      <td>2250</td>
      <td>France</td>
      <td>0</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>669</th>
      <td>20320</td>
      <td>Franche-Comte,France</td>
      <td>2250</td>
      <td>[2250]</td>
    </tr>
    <tr>
      <th>675</th>
      <td>20326</td>
      <td>Nord-Pas-de-Calais,France</td>
      <td>2250</td>
      <td>[2250]</td>
    </tr>
    <tr>
      <th>674</th>
      <td>20325</td>
      <td>Midi-Pyrenees,France</td>
      <td>2250</td>
      <td>[2250]</td>
    </tr>
    <tr>
      <th>673</th>
      <td>20324</td>
      <td>Lorraine,France</td>
      <td>2250</td>
      <td>[2250]</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3088</th>
      <td>9056091</td>
      <td>73370,Auvergne-Rhone-Alpes,France</td>
      <td>9069525</td>
      <td>[9069525, 2250]</td>
    </tr>
    <tr>
      <th>3089</th>
      <td>9056092</td>
      <td>73400,Auvergne-Rhone-Alpes,France</td>
      <td>9069525</td>
      <td>[9069525, 2250]</td>
    </tr>
    <tr>
      <th>3090</th>
      <td>9056093</td>
      <td>73600,Auvergne-Rhone-Alpes,France</td>
      <td>9069525</td>
      <td>[9069525, 2250]</td>
    </tr>
    <tr>
      <th>638</th>
      <td>1006423</td>
      <td>Saint-Agreve,Auvergne-Rhone-Alpes,France</td>
      <td>9069525</td>
      <td>[9069525, 2250]</td>
    </tr>
    <tr>
      <th>3112</th>
      <td>9056115</td>
      <td>74500,Auvergne-Rhone-Alpes,France</td>
      <td>9069525</td>
      <td>[9069525, 2250]</td>
    </tr>
  </tbody>
</table>
<p>3760 rows × 4 columns</p>
</div>

