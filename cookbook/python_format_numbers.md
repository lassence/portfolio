# Format numbers in Python

## Round decimals

```python
# Round decimals
print("{:.4f}".format(3.14159265359))
print("{:.2f}".format(3.14159265359))
print("{:.0f}".format(3.14159265359))
```

    3.1416
    3.14
    3

## Fixed width

```python
# Fixed width, including decimals
print("{:06.2f}".format(12.7649))
print("{:06.1f}".format(12.7649))
print("{:06.0f}".format(12.7649))
```

    012.76
    0012.8
    000013

## Pad integers

```python
# Padding integers
print("{:0>4d}".format(13))
print("{:->4d}".format(13))
```

    0013
    --13

## Separators for large numbers

```python
# Separators for large numbers
print("{:,.0f}".format(1079252848.85431))
```

    1,079,252,849

## Scientific notation

```python
# Scientific notation
print("{:.4e}".format(1079252848.85431))
```

    1.0793e+09

## Percentages

```python
# Percentage
print("{:.2%}".format(0.028547))
```

    2.85%

## Signed numbers

```python
# Signed numbers
print("{:+.4f}".format(8.09421))
print("{:+.4f}".format(-8.09421))
```

    +8.0942
    -8.0942

