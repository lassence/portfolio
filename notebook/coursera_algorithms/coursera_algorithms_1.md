# Coursera Algorithms part I

Code for assignments and self exploration of the excellent Coursera class [_Algorithms part I_](https://www.coursera.org/learn/algorithms-part1) by Prof. Robert Sedgewick from Princeton University.

```python
### Import libraries
import math
import random
import sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
```

## Assignement 1: percolation

```python
class UnionFind:
    
    def __init__(self, n):
        self.id = []
        self.size = [1] * n
        for i in range(0, n):
            self.id.append(i)
        print("  id =", self.id)
        print("size =", self.size)

    def root(self, i):
        while self.id[i] != i:
            i = self.id[i]
        return i
    
    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return
        else:
            if self.size[i] < self.size[j]:
                self.id[i] = j
                self.size[j] += self.size[i]
            else:
                self.id[j] = i
                self.size[i] += self.size[j]
```

```python
### Initialize object of size n**2
n = 8
grid = UnionFind(n**2)
```

```python
class Percolation:
    
    def __init__(self, n):
        self.n = n
        self.id = list(range(n**2))
        self.size = [1] * n**2
        self.state = [0] * n**2
        
    def _coord_to_ref(self, row, col):
        return (row-1) * self.n + (col-1)
    
    def _ref_to_coord(self, ref):
        return [(ref//self.n)+1, (ref%self.n)+1]
    
    def _list_open_neighbours(self, row, col):
        ref = self._coord_to_ref(row, col)
        left = (ref-1) if col > 1 else None
        right = (ref+1) if col < self.n else None
        up = ref-self.n if row > 1 else None
        down = ref+self.n if row < self.n else None
        open_neighbours = []
        for i in [left, right, up, down]:
            if i is not None and self.is_open(self._ref_to_coord(i)[0], self._ref_to_coord(i)[1]):
                open_neighbours.append(i)
        return open_neighbours
    
    def open_cell(self, row, col):
        ref = self._coord_to_ref(row, col)
        if self.state[ref] == 0:
            self.state[ref] = 1
            open_neighbours = self._list_open_neighbours(row, col)
            for neighbour in open_neighbours:
                self.union(ref, neighbour)
        
    def is_open(self, row, col):
        ref = self._coord_to_ref(row, col)
        return self.state[ref] == 1
    
    def is_full(self, row, col):
        return self.is_open(row, col) == False
    
    def number_open(self):
        return sum(self.state)
        
    def print_grid(self):
        i = 0
        while i < len(self.id):
            if self.state[i] == 1:
                print("{:3d}".format(self.root(i)), end=" ")
            else:
                print("  .", end=" ")
            if (i+1) % self.n == 0:
                print("\n")
            i += 1
            
    def root(self, i):
        while self.id[i] != i:
            i = self.id[i]
        return i            

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return
        else:
            if self.size[i] < self.size[j]:
                self.id[i] = j
                self.size[j] += self.size[i]
            else:
                self.id[j] = i
                self.size[i] += self.size[j]

    def percolated(self):
        first_row_open = [i for i in range(0, self.n) if self.state[i] == 1]
        last_row_open = [i for i in range(self.n**2-self.n, self.n**2) if self.state[i] == 1]
        for i in first_row_open:
            for j in last_row_open:
                if self.connected(i, j):
                    return True
        return False
```

```python
n = 20
perco = Percolation(n)
```

```python
for i in range(n):
    r = random.randint(1, n)
    c = random.randint(1, n)
    perco.open_cell(r, c)
print("Open sites: {:.1f}%".format(perco.number_open()/n**2*100))
print("Percolated: {}\n".format(perco.percolated()))
perco.print_grid()
```

## Week 2: Stacks and Queues

```python
class ArrayStack:
    
    def __init__(self, capacity):
        self.stack = [None] * capacity
        self.n = 0
        print(self.stack)
        
    def is_empty(self):
        return self.n == 0
    
    def push(self, item):
        self.stack[self.n] = item
        self.n = self.n + 1
        print(self.stack)
        
    def pop(self):
        self.n = max(self.n - 1, 0)
        self.stack[self.n] = None
        print(self.stack)
```

## Assignement 2: Double-Ended Queue

```python
class LinkedList:

    def __init__(self):
        self.last = self.Node(None, None)
        self.first = None
        
    def is_empty(self):
        return self.first is None
        
    def enqueue(self, item):
        self.old_last = self.last
        self.last = self.Node(item, None)
        self.old_last.next = self.last
        if self.is_empty():
            self.first = self.last
        
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            out = self.first.item
            self.first = self.first.next
            return out

    def __iter__(self):
        self.n = self.first
        return self
    
    def __next__(self):
        if self.n is not None:
            out = self.n.item
            self.n = self.n.next
            return out
        else:
            raise StopIteration
            
    class Node:
        def __init__(self, item, nxt):
            self.item = item
            self.next = nxt
```

```python
class Deque():

    def __init__(self):
        self.last = self.Node(None, None, None)
        self.first = self.Node(None, None, None)
        self.size = 0
        
    def is_empty(self):
        return self.size == 0
        
    def add_first(self, item):
        self.old_first = self.first
        self.first = self.Node(item, None, self.old_first)
        if self.is_empty():
            self.last = self.first
        else:
            self.old_first.prev = self.first
        self.size += 1
    
    def add_last(self, item):
        self.old_last = self.last
        self.last = self.Node(item, self.old_last, None)
        if self.is_empty():
            self.first = self.last
        else:
            self.old_last.next = self.last
        self.size += 1
        
    def remove_first(self):
        if self.is_empty():
            return None
        else:
            pop = self.first.item
            if self.first == self.last:
                self.first = self.last = None
            else:
                self.first = self.first.next
                self.first.prev = None
            self.size -= 1
            return pop
        
    def remove_last(self):
        if self.is_empty():
            return None
        else:
            pop = self.last.item
            if self.first == self.last:
                self.first = self.last = None
            else:
                self.last = self.last.prev
                self.last.next = None
            self.size -= 1
            return pop
    
    def __iter__(self):
        self.n = self.first
        return self
    
    def __next__(self):
        if self.n is not None:
            out = self.n.item
            self.n = self.n.next
            return out
        else:
            raise StopIteration
            
    class Node:
        def __init__(self, item, prev, nxt):
            self.item = item
            self.prev = prev
            self.next = nxt
```

## Week 3: Mergesort and Quicksort

### Mergesort

```python
def is_sorted(array):
    for i in range(1, len(array)):
        if array[i] < array[i-1]:
            return False
    return True
```

```python
def merge(a, b):
    
    aux = []
    hi = len(a) + len(b)
    i = j = 0
    
    for k in range(0, hi):
        if i >= len(a):
            aux.append(b[j])
            j += 1
        elif j >= len(b):
            aux.append(a[i])
            i += 1
        elif a[i] < b[j]:
            aux.append(a[i])
            i += 1
        else:
            aux.append(b[j])
            j += 1
    
    return aux
```

```python
### Recursive MergeSort
def merge_sort(array):
    
    if len(array) < 2:
        return array
    else:
        mid = len(array) // 2
        a = merge_sort(array[:mid])
        b = merge_sort(array[mid:])
        return merge(a, b)
```

```python
### Bottom-up MergeSort
def bu_merge_sort(array):

    length = len(array)
    size = 1
    while size < length:
        size = size * 2
        for i in range(0, length, size):
            lo = i
            mid = lo + (size // 2)
            hi = lo + size
            array[lo:hi] = merge(array[lo:mid], array[mid:hi])
    assert is_sorted(array)
    return array       
```

```python
from random import randint
s = [randint(0, 20) for i in range(0, 20)]
```

```python
print("Unsorted array:  ", s)
print("Recursive sorted:", merge_sort(s))
print("Bottom-up sorted:", bu_merge_sort(s))
```

### Quicksort

```python
class QuickSort:
    
    def __init__(self):
        return
    
    def _partition(self, a, lo, hi):
        i = lo+1
        j = hi
         
        while True:
            while a[i] < a[lo]:
                i += 1
                if i == hi:
                    break
            while a[j] >= a[lo]:
                j -= 1
                if j == lo:
                    break
            if i >= j:
                break
            a[i], a[j] = a[j], a[i]

        a[lo], a[j] = a[j], a[lo]
        return a, j

    def _sort(self, a, lo, hi):
        if hi <= lo:
            return a
        a, j = self._partition(a, lo, hi)
        self._sort(a, lo, j-1)
        self._sort(a, j+1, hi)
        return a
    
    def sort(self, a):
        self.a = list(a)
        random.shuffle(self.a)
        self.a = self._sort(self.a, 0, len(self.a)-1)
        return self.a
```

```python
qs = QuickSort()
print(qs.sort("quicksortexaample"))
```

```python
class QuickSort3Way:
    
    def __init__(self):
        return
    
    def _sort(self, a, lo, hi):
        
        if hi <= lo:
            return
        
        lt = lo
        gt = hi
        v = a[lo]
        i = lo
        
        while i <= gt:
            if a[i] < v:
                a[i], a[lt] = a[lt], a[i]
                i += 1
                lt += 1
            elif a[i] > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        
        self._sort(a, lo, lt-1)
        self._sort(a, gt+1, hi)
        return a
        
    def sort(self, a):
        self.a = list(a)
        self.a = self._sort(self.a, 0, len(self.a)-1)
        return self.a
```

```python
qs3 = QuickSort3Way()
print(qs3.sort("quicksortexaample"))
```

## Assignement 3: Collinear points

```python
### Create random points and draw graph
random.seed(22)
coords = []
i = 0
while i < 25:
    dot = (random.randint(0, 10), random.randint(0, 10))
    if dot not in coords:
        coords.append(dot)
        i += 1
pd.DataFrame(coords).plot(x=0, y=1, kind='scatter', figsize=(8,6));
```

```python
class Point:
    
    def __init__(self, xy):
        self.x, self.y = xy
        
    def coords(self):
        return (self.x, self.y)
        
    def compare_to(self, that):
        if self.y < that.y:
            return "less"
        elif self.y > that.y:
            return "more"
        elif self.y == that.y:
            if self.x < that.x:
                return "less"
            elif self.x > that.x:
                return "more"
            else:
                return "equal"

    def slope_to(self, that):
        if self.x == that.x:
            if self.y == that.y:
                return -(np.inf)
            else:
                return np.inf
        elif self.y == that.y:
            return 0
        else:
            return (that.y - self.y)/(that.x - self.x)
        
    def collinear(self, point1, point2):
        if self.slope_to(point1) == self.slope_to(point2):
            return True
        else:
            return False
```

```python
points = [Point(p) for p in coords]
```

```python
class FindSegments:
    
    def __init__(self, points):
        
        ### Compute slopes between points, for each point
        self.points = points
        self.slopes = []
        for p in self.points:
            point_slopes = []
            for q in self.points:
                point_slopes.append((q, p.slope_to(q)))
            point_slopes.sort(key=lambda tup: tup[1])
            self.slopes.append(point_slopes)
            
    def find_segments(self):
        
        ### Calculate segments
        self.all_segments = []
        for point in self.slopes:
            segments = []
            adj_points = []
            for key, value in enumerate(point):
                if key == 0:
                    previous = (None, None)
                if value[1] == previous[1]:
                    adj_points.append(previous[0])
                else:
                    if len(adj_points) >= 2:
                        adj_points.append(previous[0])
                        segments.append(adj_points)
                    adj_points = []
                previous = value
            if len(segments) > 0:
                self.all_segments.append(segments)
        return self.all_segments
```
