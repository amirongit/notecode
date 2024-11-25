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

    @property
    def top(self) -> T:
        if (value := self.inner[self.tail]) is None:
            raise IndexError

        return value
```
## Recursion
- function which calls itself untill one of the calls return due to a condition known as the base case
### Three major steps of recursion
- pre recurse
- recurse
- post recurse
#### Maze solution
```py
from copy import deepcopy
from dataclasses import dataclass
from time import sleep
from subprocess import call


@dataclass(kw_only=True)
class Point:
    x: int
    y: int


def visualize(maze: list[str], path: list[Point]) -> None:
    dis = deepcopy(maze)

    for p in path:
        dis[p.y] = dis[p.y][:p.x] + 'O' + dis[p.y][p.x + 1:]

    call('clear')
    for row in dis:
        print(row)
    sleep(.05)


def solve_maze(start: Point, end: Point, maze: list[str]) -> list[Point]:

    path: list[Point] = []

    def walk(curr: Point, seen: list[Point]) -> bool:
        if (curr.y >= len(maze) or curr.x >= len(maze[curr.y])) or maze[curr.y][curr.x] == 'X':
            return False

        if curr in seen:
            return False

        if curr == end:
            return True

        seen.append(curr)
        path.append(curr)
        for p in (
            Point(x=curr.x, y=curr.y - 1),
            Point(x=curr.x + 1, y=curr.y),
            Point(x=curr.x, y=curr.y + 1),
            Point(x=curr.x - 1, y=curr.y),
        ):
            if walk(p, seen):
                path.append(p)
                return True

        path.pop()
        return False

    walk(start, [])
    return path
```
## Quick sort
- `O(N.log(N))` to `O(N^2)`
### Divide & conquer
- spliting a problem into multiple subproblems
### Implementation
```py
def quick_sort[T: (int, float, str)](array: list[T]) -> list[T]:
    if len(array) <= 1:
        return array

    middle_index = len(array) // 2
    middle = array[middle_index]

    left = []
    right = []
    for item in array[:middle_index] + array[middle_index + 1:]:
        if item <= middle:
            left.append(item)
        else:
            right.append(item)

    return quick_sort(left) + [middle] + quick_sort(right)
```
## Trees
- tree like structures consisting of nodes having child nodes & parents
### Overview
#### Root
- the most parent node
#### Height
- number of nodes traversed to get from root to the most child node
#### Binary tree
- trees in which each node can have up to two child nodes
#### General tree
- trees in which each node can have unlimited number of child nodes
#### Leaf
- nodes without child nodes
#### Balanced binary tree
- have their subtrees
    - differ in height by at most one
    - balanced
#### Branching factor
- number of direct child nodes a node has
### Traversal
- the operation of visiting all the values of a tree
- `O(N)`
- stack data structure is implicitly being used (function call stack)
#### Pre order
- visiting current node before visiting its children
#### In order
- visiting current node in the middle of visiting its children
- usually applicable on binary trees only
#### Post order
- visiting current node after visiting its children
#### DFS
- depth first search
#### Implementation
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def pre_order[T](root: Node[T] | None = None) -> None:
    if root is None:
        return

    print(root.value)
    pre_order(root.left)
    pre_order(root.right)


def in_order[T](root: Node[T] | None = None) -> None:
    if root is None:
        return

    in_order(root.left)
    print(root.value)
    in_order(root.right)


def post_order[T](root: Node[T] | None = None) -> None:
    if root is None:
        return

    post_order(root.left)
    post_order(root.right)
    print(root.value)
```
## Tree search
### BFS
- breadth first search
#### Implementation
```py
from __future__ import annotations
from queue import Queue


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def breadth_first[T](root: Node[T]) -> None:
    q: Queue[Node[T]] = Queue(-1)

    q.put(root)
    while not q.empty():
        print((node := q.get()).value)

        if (left := node.left) is not None:
            q.put(left)

        if (right := node.right) is not None:
            q.put(right)
```
### Tree comparison
- `O(N)`
#### Implementation
```py
from __future__ import annotations
from queue import Queue


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def compare[T](first: Node[T] | None, second: Node[T] | None) -> bool:
    if first is None and second is None:
        return True
    elif first is None or second is None:
        return False
    elif first.value != second.value:
        return False

    return compare(first.left, second.left) and compare(first.right, second.right)
```
### Binary search tree
- `O(log(N))` to `O(N)`
    - O of height of tree
- given tree must be sorted
#### Implementation
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def binary_search[T: (int, float, str)](tree: Node[T], value: T) -> bool:
    if tree.value == value:
        return True
    elif tree.value > value:
        return False if tree.left is None else binary_search(tree.left, value)
    else:
        return False if tree.right is None else binary_search(tree.right, value)
```
### Binary tree insertion
- `O(log(N))` to `O(N)`
    - O of height of tree
- given tree must be sorted
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def insert[T: (int, float, str)](tree: Node[T], value: T) -> None:
    if value <= tree.value:
        if tree.left is None:
            tree.left = Node(value)
        else:
            insert(tree.left, value)
    else:
        if tree.right is None:
            tree.right = Node(value)
        else:
            insert(tree.right, value)
```
### Binary tree deletion
- implementing it made me age
#### Implementation
```py
from __future__ import annotations
from typing import Literal, TypeAlias
from random import choice


Path: TypeAlias = tuple[Literal['l'] | Literal['r'], ...]


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return str(self.value)


def delete[T](root: Node[T], path: Path) -> None:
    if len(path) < 1:
        raise RuntimeError

    node = get(root, path)
    parent = get(root, path[:-1])
    node_dir = path[-1]

    if (node.left is not None) is not (node.right is not None):
        if node.left is not None:
            child = node.left
            node.left = None
        else:
            child = node.right
            node.right = None
        if node_dir == 'l':
            parent.left = child
        else:
            parent.right = child
    elif node.left is None and node.right is None:
        if node_dir == 'l':
            parent.left = None
        else:
            parent.right = None
    else:
        if choice((False, True)):
            last_node, last_node_path = lowest(node.right) # type: ignore
            delete(node, ('r',) + last_node_path)
        else:
            last_node, last_node_path = highest(node.left) # type: ignore
            delete(node, ('l',) + last_node_path)
        if node_dir == 'l':
            parent.left.value = last_node.value # type: ignore
        else:
            parent.right.value = last_node.value # type: ignore


def lowest[T](root: Node[T]) -> tuple[Node[T], Path]:
    node = root
    path: Path = ()
    while node.left is not None:
        node = node.left
        path += ('l',) # type: ignore
    return node, path


def highest[T](root: Node[T]) -> tuple[Node[T], Path]:
    node = root
    path: Path = ()
    while node.right is not None:
        node = node.right
        path += ('r',) # type: ignore
    return node, path


def get[T](root: Node[T], path: Path) -> Node[T]:
    node: Node[T] = root
    for direction in path:
        if direction == 'l':
            node = node.left # type: ignore
        else:
            node = node.right # type: ignore
    return node
```
