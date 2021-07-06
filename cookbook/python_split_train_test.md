# Split data into training and test sets

When randomly splitting a dataset for Machine Learning into training and test sets, several methods can be used.

```python
# Import libraries
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
```

## Load dataset

```python
# Load sample dataset into a DataFrame
X = sns.load_dataset('iris')

# Pop the target column and store in a distinct Series
y = X.pop('species')

# Check shapes
print("X:", X.shape)
print("y:", y.shape)
```

    X: (150, 4)
    y: (150,)

## Method 1: using scikit-learn

```python
# Use `train_test_split()` function to extract a random test set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

If the parameter `test_size` is not specified, the test set will get 25% of the rows by default.

```python
# Check shapes of sets
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)
```

    X_train: (120, 4)
    y_train: (120,)
    X_test: (30, 4)
    y_test: (30,)

## Method 2: using pandas

```python
# Extract random rows for test set with `sample()`
X_test = X.sample(frac=0.20)
y_test = y.loc[y.index.isin(X_test.index)]

# Remaining rows are for the training test
X_train = X.loc[~X.index.isin(X_test.index)]
y_train = y.loc[~y.index.isin(X_test.index)]
```

```python
# Check shapes of sets
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)
```

    X_train: (120, 4)
    y_train: (120,)
    X_test: (30, 4)
    y_test: (30,)

