# Convert nested string field to dict

When importing data from a tabular file, you may have nested fields inside a column. To work with them, you first need to convert them to a proper dictionary. This can be done using `json.loads`.

```python
# Import libraries
import json
import pandas as pd

# Load sample JSON data
df = pd.read_csv('data/dict.csv', sep=';')
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>place</th>
      <th>grades</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Ariel</td>
      <td>{"count": 12,"value": 4.3}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Nerval</td>
      <td>{"count": 8,"value": 3.9}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Zigzag</td>
      <td>{"count": 24,"value": 2.8}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Camelia</td>
      <td>{"count": 16,"value": 3.1}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Big Ben</td>
      <td>{"count": 4,"value": 3.7}</td>
    </tr>
  </tbody>
</table>
</div>

```python
# Convert nested column to a dict
df['grades'] = df['grades'].apply(json.loads)
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>place</th>
      <th>grades</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Ariel</td>
      <td>{'count': 12, 'value': 4.3}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Nerval</td>
      <td>{'count': 8, 'value': 3.9}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Zigzag</td>
      <td>{'count': 24, 'value': 2.8}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Camelia</td>
      <td>{'count': 16, 'value': 3.1}</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Big Ben</td>
      <td>{'count': 4, 'value': 3.7}</td>
    </tr>
  </tbody>
</table>
</div>

```python
# You can now read the dict inside the column
df['grade_count']  = df['grades'].apply(lambda x: x['count'])
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>place</th>
      <th>grades</th>
      <th>grade_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Ariel</td>
      <td>{'count': 12, 'value': 4.3}</td>
      <td>12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Nerval</td>
      <td>{'count': 8, 'value': 3.9}</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Zigzag</td>
      <td>{'count': 24, 'value': 2.8}</td>
      <td>24</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Camelia</td>
      <td>{'count': 16, 'value': 3.1}</td>
      <td>16</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Big Ben</td>
      <td>{'count': 4, 'value': 3.7}</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>

