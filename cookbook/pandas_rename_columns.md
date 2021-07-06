# Rename columns in method chaining

When I need to apply successive steps of data transformation to a DataFrame (i.e. basically in every data analysis), I favor [method chaining](https://tomaugspurger.github.io/method-chaining) for better readability and efficiency. However, some operations stayed rather obscure to me for a long time, like renaming all columns in a single operation. Here are some tips that may come in handy.

## Setup

```python
# Import library
import pandas as pd

# Create sample DataFrame
df = pd.DataFrame({'First Name': ['John', 'Aby', 'Bob', 'Alice'],
                  'Last Name': ['Doe', 'Parker', 'Morris', 'Allen']})
df
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>First Name</th>
      <th>Last Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>John</td>
      <td>Doe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aby</td>
      <td>Parker</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bob</td>
      <td>Morris</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>Allen</td>
    </tr>
  </tbody>
</table>
</div>

## Classic, non-chained method

A standard way of applying transformative functions to all columns names would be the following:

```python
# Classic way
df2 = df.copy()
df2.columns = [col.lower().replace(' ', '_') for col in df2.columns]
df2
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first_name</th>
      <th>last_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>John</td>
      <td>Doe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aby</td>
      <td>Parker</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bob</td>
      <td>Morris</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>Allen</td>
    </tr>
  </tbody>
</table>
</div>

## Apply transformative functions

With pandas method chaining, you can apply functions to transform names with `.rename(columns=<function>)`.

Applying a function that does not require any argument, like `lower()` or `title()`, is very short:

```python
# Method chaining: convert to lowercase
df.rename(columns=str.lower)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first name</th>
      <th>last name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>John</td>
      <td>Doe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aby</td>
      <td>Parker</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bob</td>
      <td>Morris</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>Allen</td>
    </tr>
  </tbody>
</table>
</div>

For a function that requires arguments, like `str.replace()`, use a `lambda`:

```python
# Method chaining: replace strings
df.rename(columns=lambda x: x.replace(' ', ''))
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>FirstName</th>
      <th>LastName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>John</td>
      <td>Doe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aby</td>
      <td>Parker</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bob</td>
      <td>Morris</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>Allen</td>
    </tr>
  </tbody>
</table>
</div>

## Specify new names to columns

If you want to specify a list of new columns names, use `set_axis()`:

```python
# Method chaining: rename all columns
df.set_axis(['given_name', 'family_name'], axis=1)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>given_name</th>
      <th>family_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>John</td>
      <td>Doe</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aby</td>
      <td>Parker</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bob</td>
      <td>Morris</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alice</td>
      <td>Allen</td>
    </tr>
  </tbody>
</table>
</div>

