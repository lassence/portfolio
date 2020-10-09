# Get common elements between two Python lists

When you want to get the intersection (common elements) between two or more lists, an easy way in Python is to convert your lists to **sets** and use `intersection()`. Note that it will remove any duplicates, and return only unique elements.


```python
# Two lists
a = ['apple', 'pear', 'orange', 'kiwi', 'banana', 'lemon']
b = ['melon', 'lemon', 'strawberry', 'kiwi']

# Get intersection
set(a).intersection(set(b))
```




    {'kiwi', 'lemon'}



You can also get elements that are *not* common between the lists:


```python
# Get difference
set(a).difference(set(b))
```




    {'apple', 'banana', 'orange', 'pear'}


