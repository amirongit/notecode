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
```py
# cool, but `O(N)`
def binary_search[T: (int, float, str)](array: list[T], value: T) -> bool:
    return (
        False if (length := len(array)) == 0 else
        True if (middle_item := array[(middle_index := length // 2)]) == value else
        binary_search(array[:middle_index], value) if middle_item > value else
        binary_search(array[middle_index + 1:], value)
    )

# boring, but `O(log(N))`
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
- `O(N)` for acquirement
- insertino & deletion
    - `O(1)` without acquirement
    - `O(N)` with acquirement
#### Singly linked list
- each container points to its next container only
#### Doubly linked list
- each container points to its next & previous containers
#### Implementation
```py
from __future__ import annotations

class Node[T]:
    def __init__(self, value: T, *, previous: Node[T] | None = None, next: Node[T] | None = None) -> None:
        self.value = value
        self.next = next
        self.prev = previous

class LinkedList[T]:
    def __init__(self, *values: T) -> None:
        if len(values) > 0:
            self.head = Node(values[0])
            self.length = 1

        if len(values) > 1:
            for index, value in enumerate(values[1:]):
                self.insert(value, index + 1)

    def insert(self, value: T, index: int) -> None:
        if index == 0:
            next_ = self._get_node(index)
            next_.prev = Node(value, next=next_)
            self.head = next_.prev
        elif index == len(self):
            prev = self._get_node(index - 1)
            prev.next = Node(value, previous=prev)
        else:
            next_ = self._get_node(index)
            prev = self._get_node(index - 1)
            current = Node(value, previous=prev, next=next_)
            next_.prev = current
            prev.next = current

        self.length += 1

    def delete(self, index: int) -> None:
        if index == 0 and len(self) == 1:
            raise ValueError

        node = self._get_node(index)
        next_ = node.next
        prev = node.prev

        if next_ is not None:
            next_.prev = prev

        if prev is not None:
            prev.next = next_

        if index == 0:
            self.head = next_

        node.next = None
        node.prev = None
        self.length -= 1

    def _get_node(self, index: int) -> Node[T]:
        if len(self) == 0 or self.head is None:
            raise IndexError

        if index == 0:
            return self.head

        node = self.head
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
        return self.length

    def __iter__(self):
        self._current_loop = self.head
        return self

    def __next__(self):
        if (holder := self._current_loop) is None:
            raise StopIteration

        self._current_loop = holder.next

        return holder.value

    def __str__(self) -> str:
        return '<->'.join((str(n) for n in self))
```
### Queue data structure
- FIFO linked list without traversing
- `O(1)` for pushing & popping
#### FIFO structure
- what goes first, comes out first
#### Implementation
```py
from __future__ import annotations

class Node[T]:
    def __init__(self, value: T, *, next: Node[T] | None = None, prev: Node[T] | None = None) -> None:
        self.value = value
        self.next = next
        self.prev = prev


class Queue[T]:
    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self.length = 0

    def lpush(self, value: T) -> None:
        if self.tail is None:
            genesis = Node(value)
            self.head = genesis
            self.tail = genesis
        elif self.head is None:
            raise RuntimeError
        else:
            current = self.head
            new = Node(value, next=current)
            current.prev = new
            self.head = new

        self.length += 1;

    def rpush(self, value: T) -> None:
        if self.head is None:
            genesis = Node(value)
            self.head = genesis
            self.tail = genesis
        elif self.tail is None:
            raise RuntimeError
        else:
            current = self.tail
            new = Node(value, prev=current)
            current.next = new
            self.tail = new

        self.length += 1;

    def lpop(self) -> T:
        if (current := self.head) is None:
            raise ValueError

        
        if (next := current.next) is not None:
            next.prev = None
            self.head = next

        self.length -= 1;
        return current.value

    def rpop(self) -> T:
        if (current := self.tail) is None:
            raise ValueError

        if (prev := current.prev) is not None:
            prev.next = None
            self.tail = prev

        self.length -= 1;
        return current.value

    def __len__(self) -> int:
        return self.length

    @property
    def right(self) -> T | None:
        return self.tail.value if self.tail is not None else None

    @property
    def left(self) -> T | None:
        return self.head.value if self.head is not None else None
```
### Stack data structure
- FILO linked list without traversing
- `O(1)` for pushing & popping
#### FILO structure
- what goes first, comes out last
#### Implementation
```py
from __future__ import annotations

class Node[T]:
    def __init__(self, value: T, *, previous: Node[T] | None = None) -> None:
        self.value = value
        self.prev = previous


class Stack[T]:
    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.length = 0

    def push(self, value: T) -> None:
        self.head = Node(value, previous=self.head)
        self.length += 1

    def pop(self) -> T:
        if self.head is None:
            raise ValueError

        current = self.head
        self.head = current.prev
        self.length -= 1

        return current.value

    @property
    def top(self) -> T | None:
        return self.head.value if self.head is not None else None

    def __len__(self) -> int:
        return self.length
```
