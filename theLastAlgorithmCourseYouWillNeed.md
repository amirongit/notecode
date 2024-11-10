# The Last Algorithm Course You Will Need
## Basics
### Big O notation
- shows growth rate of algorithm as its input does
- 'n' & 'm' are used to denote input size
- constants (coefficient & lower terms) aren't considered
    - the point is to measure growth rate generally
    - if input size doesn't affect the growth rate, remaining constants are reduced to 1
    - constants are important practically
- often the worst case scenario is calculated
### Array data structure
- fixed size contiguous block of memory
- segmented by units called elements
- elements are accessed by indices
- assigning elements
    - writing data on bits of their segments
- deleting elements
    - well each lang does it in its own way!
    - usually an special under the hood insertion
- big O of assigning & deleting an element in an array?
    - `read(starting point + index * segment width)`
    - `O(1)`
## Search
### Linear search
- `O(N)`
#### Implementation
```py
def linear_search[T](array: Iterable[T], value: T) -> bool:
    for item in array:
        if item == value:
            return True
    return False
```
### Binary search
- `O(log(N))`
- given array must be sorted
#### Implementation
##### cool, but `O(N)`
```py
def binary_search[T: (int, float, str)](array: list[T], value: T) -> bool:
    return (
        False if (length := len(array)) == 0 else
        True if (middle_item := array[(middle_index := length // 2)]) == value else
        binary_search(array[:middle_index], value) if middle_item > value else
        binary_search(array[middle_index + 1:], value)
    )
```
##### boring, but `O(log(N))`
```py
def binary_search[T: (int, float, str)](array: list[T], value: T) -> bool:
    fi = 0
    li = len(array)
    while (length := abs(fi - li)) > 0:
        if (mv := array[(si := fi + (length // 2))]) == value:
            return True
        elif mv > value:
            li = si
        elif mv < value:
            fi = si + 1

    return False
```
## Sort
### Bubble sort
- `O(N^2)`
#### Implementation
```py
def bubble_sort[T: (int, float, str)](array: list[T]) -> list[T]:
    from copy import deepcopy
    array_ = deepcopy(array)

    li = len(array_) - 1
    while li != 0:
        fi = 0
        while fi < li:
            if (array_[fi] > array_[fi + 1]):
                array_[fi], array_[fi + 1] = array_[fi + 1], array_[fi]
            fi += 1
        li -= 1

    return array_
```
### Linked list data structure
- made of containers which hold values & pointers to other containers
#### Singly linked list
- each container points to its next container only
#### Dobly linked list
- each container points to its next & previous containers
##### Implementation
```py
from __future__ import annotations

class Node[T]:
    def __init__(self, value: T, *, previous: Node[T] | None = None, next: Node[T] | None = None) -> None:
        self._value = value
        self._next = next
        self._previous = previous

    @property
    def value(self) -> T:
        return self._value

    @property
    def previous(self) -> Node[T] | None:
        return self._previous

    @property
    def next(self) -> Node[T] | None:
        return self._next

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node) or not isinstance(other.value, type(self.value)):
            return False

        return id(self.next) == id(other.next) and id(self.previous) == id(other.previous) and self.value == other.value


class LinkedList[T]:
    def __init__(self, *values: T) -> None:
        if len(values) > 0:
            self._head = Node(values[0])
            self._length = 1

        if len(values) > 1:
            for index, value in enumerate(values[1:]):
                self.insert(value, index + 1)

    def insert(self, value: T, index: int) -> None:
        if index == 0:
            next_ = self._get_node(index)
            next_._previous = Node(value, next=next_)
            self._head = next_.previous
        elif index == len(self):
            prev = self._get_node(index - 1)
            prev._next = Node(value, previous=prev)
        else:
            next_ = self._get_node(index)
            prev = self._get_node(index - 1)
            current = Node(value, previous=prev, next=next_)
            next_._previous = current
            prev._next = current

        self._length += 1

    @property
    def head(self) -> T | None:
        return self._head.value if self._head is not None else None

    def _get_node(self, index: int) -> Node[T]:
        if len(self) == 0 or self._head is None:
            raise IndexError

        if index == 0:
            return self._head

        node = self._head
        counter = 0

        while counter < index:
            if node.next is None:
                raise IndexError

            node = node.next
            counter += 1

        return node

    def __getitem__(self, index: int) -> T:
        return self._get_node(index).value

    def __len__(self) -> int:
        return self._length

    def __iter__(self):
        self._current_loop = self._head
        return self

    def __next__(self):
        if (holder := self._current_loop) is None:
            raise StopIteration

        self._current_loop = holder.next

        return holder.value

    def __str__(self) -> str:
        return '<->'.join((str(n) for n in self))
```
