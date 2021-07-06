# Jupyter magic commands for BigQuery

To avoid boilerplate code in Jupyter notebooks, it is possible to use [magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html) with the BigQuery library.

This simplifies the code from this:

```python
sql = """
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 5
"""

(
    bqclient
    .query(sql)
    .result()
    .to_dataframe()
)
```

to this:

```python
%%bigquery
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 5
```

## Load module

If you run a cloud-based JupyterLab notebook with AI Platform, you won't need this step, as the BigQuery module is already installed and loaded.

Otherwise, open a Jupyter notebook. 
Make sure you have installed the [*google-cloud-bigquery*](https://pypi.org/project/google-cloud-bigquery/) Python library. 
Load the magic commands module with the following:

```python
# Load magic commands from the library
%load_ext google.cloud.bigquery
```

## Run query in a magic cell

Create a magic cell with `%%bigquery` on the first line (don't add anything above, not even commented lines) and directly enter your query below:

```python
%%bigquery
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 5
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>birth_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2008</td>
      <td>4255156</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007</td>
      <td>4324008</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2006</td>
      <td>4273225</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2005</td>
      <td>4145619</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2004</td>
      <td>4118907</td>
    </tr>
  </tbody>
</table>
</div>

## Magic command options

To save the results to a pandas DataFrame instead of displaying them directly, add a variable name after `%%bigquery`

```python
%%bigquery df
# Save results to `df`
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT 5
```

```python
# Print the resulting DataFrame
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>birth_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2008</td>
      <td>4255156</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007</td>
      <td>4324008</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2006</td>
      <td>4273225</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2005</td>
      <td>4145619</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2004</td>
      <td>4118907</td>
    </tr>
  </tbody>
</table>
</div>

It is possible to set parameters with `--params`, and use them in the query with `@param`:

```python
%%bigquery --params {"lim": 10}
# Use a parameter for query limit
SELECT
    source_year AS year,
    COUNT(is_male) AS birth_count
FROM `bigquery-public-data.samples.natality`
GROUP BY year
ORDER BY year DESC
LIMIT @lim
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>birth_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2008</td>
      <td>4255156</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2007</td>
      <td>4324008</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2006</td>
      <td>4273225</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2005</td>
      <td>4145619</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2004</td>
      <td>4118907</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2003</td>
      <td>4096092</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2002</td>
      <td>4027376</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2001</td>
      <td>4031531</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2000</td>
      <td>4063823</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1999</td>
      <td>3963465</td>
    </tr>
  </tbody>
</table>
</div>

