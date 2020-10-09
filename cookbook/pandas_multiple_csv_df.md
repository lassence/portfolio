# Read multiple CSV files into a pandas DataFrame

Here is how to ingest multiple CSV files with the same structure into one DataFrame:

```python
# Import libraries
import pandas as pd

# List of files
files = [
    'data_1.csv',
    'data_2.csv',
    'data_3.csv',
    'data_4.csv',
    'data_5.csv'
]

# Read each CSV file and append its content to `df`
df = pd.DataFrame()
for f in files:
    df = df.append(pd.read_csv(f))
```
