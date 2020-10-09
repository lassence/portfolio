# List files in a folder with Python

Listing files in a folder can be done with the `os` or `glob` library in Python.

## List all files in a folder

```python
# List all files
import os
folder = 'my_data'
files_list = [f for f in os.listdir(folder)]
```

## List files that match a condition

```python
# List files which name ends with `.txt`
import os
folder = 'my_data'
files_list = [f for f in os.listdir(folder) if f.endswith('.txt')]
```

Alternatively, you can use the `glob` library.

```python
# List files which name contains `_log_`
import glob
folder = 'my_data/'
files_list = glob.glob(folder + '*_log_*')
```

## Recursively find files in subfolders

To find all files in subfolders, the easiest way since Python 3.5 is to use `glob.glob()` with the `recursive` parameter.

```python
# List CSV files which name contains `_log_`, also searching in subfolders
import glob
folder = 'my_data/'
files_list = glob.glob(folder + '/**/*_log_*.csv', recursive=True)
```
