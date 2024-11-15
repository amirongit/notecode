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
- growable sequence made of containers which hold values & pointers to other containers
- `O(N)` for random access
- `O(N)` for insertion
- `O(N)` for deletion
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
            next_ = self.get_node(index)
            next_.prev = Node(value, next=next_)
            self.head = next_.prev
        elif index == len(self):
            prev = self.get_node(index - 1)
            prev.next = Node(value, previous=prev)
        else:
            next_ = self.get_node(index)
            prev = self.get_node(index - 1)
            current = Node(value, previous=prev, next=next_)
            next_.prev = current
            prev.next = current

        self.length += 1

    def delete(self, index: int) -> None:
        if index == 0 and len(self) == 1:
            raise ValueError

        node = self.get_node(index)
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
        return self.get_node(index).value

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> LinkedList[T]:
        self.current_loop = self.head
        return self

    def __next__(self) -> T:
        if (holder := self.current_loop) is None:
            raise StopIteration

        self.current_loop = holder.next

        return holder.value

    def __str__(self) -> str:
        return '<->'.join((str(n) for n in self))
```
### Queue data structure
- FIFO linked list without traversing
- `O(1)` for pushing
- `O(1)` for popping
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
## Arrays
### Array list
- maintains an array which increases its size upon reaching its capacity
- `O(1)` for random access
- `O(1)` for assignment
- `O(N)` for insertion
- `O(N)` for prepending
- appending
    - mostly (on average) `O(1)`
    - increasing size requires copying all elements which is `O(N)`
    - it's considered to be `O(1)` due to something called amortized analysis!
#### Implementation
```py
from __future__ import annotations


class FakeArray[T]:
    def __init__(self, length: int) -> None:
        if length < 0:
            raise ValueError

        self.inner: dict[int, T | None] = {}
        self.length = length

    def __getitem__(self, index: int) -> T | None:
        if index > self.length:
            raise IndexError

        return self.inner.get(index)

    def __setitem__(self, index: int, item: T | None) -> None:
        if index > self.length or index < 0:
            raise IndexError

        self.inner[index] = item

    def __iter__(self) -> FakeArray[T]:
        self.current_loop = 0
        return self

    def __next__(self) -> T | None:
        try:
            val = self[self.current_loop]
            self.current_loop += 1
            return val
        except IndexError:
            raise StopIteration

    def __str__(self) -> str:
        return ', '.join(str(i) for i in self)

    def __repr__(self) -> str:
        return str(self)


class ArrayList[T]:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.length = 0
        self.inner: FakeArray[T] = FakeArray(capacity)

    def append(self, value: T) -> None:
        if self.length - 1 == self.capacity:
            self.extend_array()

        self.inner[self.length] = value
        self.length += 1

    def prepend(self, value: T) -> None:
        if self.length - 1 == self.capacity:
            self.extend_array()

        self.inner = ArrayList.shift_right(self.inner)
        self.inner[0] = value
        self.length += 1

    def insert(self, index: int, value: T) -> None:
        if self.length - 1 == self.capacity:
            self.extend_array()

        self.inner = ArrayList.shift_right(self.inner, index)
        self.inner[index] = value
        self.length += 1

    def extend_array(self) -> None:
        self.capacity *= 2
        new: FakeArray[T] = FakeArray(self.capacity)
        for i, v in enumerate(self.inner):
            new[i] = v
        self.inner = new

    @staticmethod
    def shift_right[TA](array: FakeArray[TA], offset: int = 0) -> FakeArray[TA]:
        new: FakeArray[TA] = FakeArray(array.length)

        if len(keys := array.inner.keys()) == 0:
            return new

        for i in range(offset):
            new[i] = array[i]

        for i in range(max(keys), offset - 1, -1):
            new[i + 1] = array[i]

        return new

    def __getitem__(self, index: int) -> T | None:
        self.inner[index]

    def __setitem__(self, index: int, value: T | None) -> None:
        self.inner[index] = value

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return str(self.inner)

    def __repr__(self) -> str:
        return repr(self.inner)
```
### Array buffer
- fixed size queue implemented on arrays
- `O(1)` for pushing
- `O(1)` for popping
- `O(1)` for random access
#### Implementation
```py
from __future__ import annotations


class FakeArray[T]:
    def __init__(self, length: int) -> None:
        if length < 0:
            raise ValueError

        self.inner: dict[int, T | None] = {}
        self.length = length

    def __getitem__(self, index: int) -> T | None:
        if index > self.length:
            raise IndexError

        return self.inner.get(index)

    def __setitem__(self, index: int, item: T | None) -> None:
        if index > self.length or index < 0:
            raise IndexError

        self.inner[index] = item

    def __iter__(self) -> FakeArray[T]:
        self.current_loop = 0
        return self

    def __next__(self) -> T | None:
        try:
            val = self[self.current_loop]
            self.current_loop += 1
            return val
        except IndexError:
            raise StopIteration

    def __str__(self) -> str:
        return ', '.join(str(i) for i in self)

    def __repr__(self) -> str:
        return str(self)


class RingBuffer[T]:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.length = 0
        self.head = -1
        self.tail = -1
        self.inner: FakeArray[T] = FakeArray(capacity)

    def push(self, value: T) -> None:
        if self.capacity == self.length - 1:
            raise OverflowError

        self.inner[index := (self.tail + 1) % (self.capacity + 1)] = value
        self.tail = index
        self.length += 1

        if self.length == 1:
            self.head += 1

    def pop(self) -> T:
        if (value := self.inner[(index := self.head)]) is None:
            raise IndexError

        self.inner[index] = None
        self.head += 1
        self.length -= 1

        return value

    def __getitem__(self, index: int) -> T | None:
        return self.inner[index if index < self.capacity else index % self.capacity]

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return str(self.inner)

    def __repr__(self) -> str:
        return repr(self.inner)

    @property
    def top(self) -> T:
        if (value := self.inner[self.tail]) is None:
            raise IndexError

        return value
```
