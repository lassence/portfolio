# Flatten JSON files with pandas

Flattening nested JSON data and export it to CSV can often be done easily with pandas Series.

## Setup


```python
# Load libraries
import pandas as pd
import json
```


```python
# Load JSON file as a Dict
with open('data/nested.json') as f:
    raw = json.load(f)

raw
```




    {'header': 'title',
     'stuff': {'intro': 'hello',
      'onetype': {'id': 1, 'name': 'John Doe'},
      'othertype': {'id': 2, 'company': 'ACME'}},
     'otherstuff': {'thing': {'first': 'this', 'second': 'that'}}}




```python
# Flatten JSON, with field names separated with a dot
flat = pd.Series(pd.json_normalize(raw, sep='.').to_dict(orient='records')[0])
flat
```




    header                        title
    stuff.intro                   hello
    stuff.onetype.id                  1
    stuff.onetype.name         John Doe
    stuff.othertype.id                2
    stuff.othertype.company        ACME
    otherstuff.thing.first         this
    otherstuff.thing.second        that
    dtype: object




```python
# Export to CSV
pd.Series(flat).to_csv('data/flat.csv')
```
