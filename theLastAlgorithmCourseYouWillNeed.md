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

from lldoublenode import Node

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

from lldoublenode import Node


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

        self.length += 1

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

        self.length += 1

    def lpop(self) -> T:
        if (current := self.head) is None:
            raise ValueError


        if (next := current.next) is not None:
            next.prev = None
            self.head = next

        self.length -= 1
        return current.value

    def rpop(self) -> T:
        if (current := self.tail) is None:
            raise ValueError

        if (prev := current.prev) is not None:
            prev.next = None
            self.tail = prev

        self.length -= 1
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

from llsinglenode import Node


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

from fakearray import FakeArray


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
        return self.inner[index]

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

from fakearray import FakeArray


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

from btnode import Node


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

from btnode import Node


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

from btnode import Node


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

from btnode import Node


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

from btnode import Node


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
- `O(N)`
#### Implementation
```py
from __future__ import annotations

from random import choice
from typing import Literal

from btnode import Node

type Path = tuple[Literal["l"] | Literal["r"], ...]


def delete[T](root: Node[T], path: Path) -> None:
    if len(path) < 1:
        raise RuntimeError

    target = get(root, path)
    parent = get(root, path[:-1])
    last_dir = path[-1]

    if target.right is None or target.left is None:
        replace_node(
            parent,
            (
                None
                if target.left is None and target.right is None
                else target.right if target.left is None else target.left
            ),
            last_dir,
        )
    else:
        if choice((True, False)):
            repl, repl_path = lowest(target.right)
            delete(target, ("r",) + repl_path)  # type: ignore
        else:
            repl, repl_path = highest(target.left)
            delete(target, ("l",) + repl_path)  # type: ignore

        replace_val(parent, repl, last_dir)


def replace_node[T](parent: Node[T], repl: Node[T] | None, dir_: Direction) -> None:
    if dir_ == "l":
        parent.left = repl
    else:
        parent.right = repl


def replace_val[T](parent: Node[T], repl: Node[T], dir_: Direction) -> None:
    if dir_ == "l":
        if parent.left is None:
            raise RuntimeError
        parent.left.value = repl.value
    else:
        if parent.right is None:
            raise RuntimeError
        parent.right.value = repl.value


def lowest[T](root: Node[T]) -> tuple[Node[T], Path]:
    node = root
    path: Path = ()
    while node.left is not None:
        node = node.left
        path += ("l",)  # type: ignore
    return node, path


def highest[T](root: Node[T]) -> tuple[Node[T], Path]:
    node = root
    path: Path = ()
    while node.right is not None:
        node = node.right
        path += ("r",)  # type: ignore
    return node, path


def get[T](root: Node[T], path: Path) -> Node[T]:
    node: Node[T] = root
    for direction in path:
        if direction == "l":
            if node.left is None:
                raise RuntimeError
            node = node.left
        else:
            if node.right is None:
                raise RuntimeError
            node = node.right
    return node
```
### Binary tree visualization
- did it!
#### Implementation
```py
from __future__ import annotations

from queue import Queue
from typing import Any

from btnode import Node

type Coordinate = tuple[int, int]


def visualize[T](root: Node[T]) -> None:
    val_coor = get_coordinates(root)
    val_size = max(max(len(str(i[0])) for i in val_coor), 5)
    grid_hei = (root_hei := get_height(root)) * 2 - 1
    grid_mid = (grid_wid := 2**root_hei) // 2
    grid = [[" " * val_size for _ in range(grid_wid)] for _ in range(grid_hei)]

    for i in val_coor:
        val, y, x = i[0], abs(i[1][1]) * 2, grid_mid - i[1][0]
        grid[y][x] = f'({str(val).rjust(val_size - 2, "_")})'

        if y < grid_hei - 1:
            grid[y + 1][x] = "/" + grid[y + 1][x][1:-1] + "\\"

    print("\n".join(["".join(col) for col in grid]))


def get_coordinates[T](root: Node[T]) -> set[tuple[T, Coordinate]]:
    q: Queue[tuple[Node[T], Coordinate]] = Queue()
    coordinates = set()

    q.put((root, (0, 0)))
    while not q.empty():
        node = q.get()
        coordinates.add((node[0].value, node[1]))

        if (left := node[0].left) is not None:
            q.put((left, (node[1][0] + (2 ** (get_height(node[0].left) - 1)), node[1][1] - 1)))

        if (right := node[0].right) is not None:
            q.put((right, (node[1][0] - (2 ** (get_height(node[0].right) - 1)), node[1][1] - 1)))

    return coordinates


def get_height(root: Node[Any] | None, current: int = 0) -> int:
    if root is None:
        return current

    current += 1
    return max(get_height(root.left, current), get_height(root.right, current))
```
## Heap
- representing a tree like structure by abstracting a weakly sorted array
### Heapify
- swapping a heap element with other elements to make the tree conditions true
- `O(log(N))`
### Min heap
- every parent is less than or equal to its childrend
#### Implementation
```py
from baseheap import BaseHeap, NodeID


class MinHeap[T: (int, float, str)](BaseHeap[T]):
    def heapify_up(self, addr: NodeID) -> None:
        current, parent = (
            self.array[ci := BaseHeap.resolve(addr) if isinstance(addr, tuple) else addr],
            self.array[pi := BaseHeap.get_up(ci)],
        )
        while current is not None and parent is not None and parent > current:
            self.array[pi], self.array[ci] = current, parent
            current, parent = self.array[ci := pi], self.array[pi := BaseHeap.get_up(ci)]

    def heapify_down(self, addr: NodeID) -> None:
        current = self.array[ci := BaseHeap.resolve(addr) if isinstance(addr, tuple) else addr]
        (left, li), (right, ri) = self.get_children(ci)
        gleft = current is not None and left is not None and left < current
        gright = current is not None and right is not None and right < current
        while gleft or gright:
            if gleft and gright:
                if min(right, left) == right:  # type: ignore
                    gleft = False
                else:
                    gright = False

            if gleft:
                self.array[ci], self.array[ci := li] = left, current
            else:
                self.array[ci], self.array[ci := ri] = right, current

            current = self.array[ci]
            (left, li), (right, ri) = self.get_children(ci)
            gleft = current is not None and left is not None and left < current
            gright = current is not None and right is not None and right < current
```
### Max heap
- every parent is greater than or equal to its childrend
#### Implementation
```py
from baseheap import BaseHeap, NodeID


class MaxHeap[T: (int, float, str)](BaseHeap[T]):
    def heapify_up(self, addr: NodeID) -> None:
        current, parent = (
            self.array[ci := BaseHeap.resolve(addr) if isinstance(addr, tuple) else addr],
            self.array[pi := BaseHeap.get_up(ci)],
        )
        while current is not None and parent is not None and parent < current:
            self.array[pi], self.array[ci] = current, parent
            current, parent = self.array[ci := pi], self.array[pi := BaseHeap.get_up(ci)]

    def heapify_down(self, addr: NodeID) -> None:
        current = self.array[ci := BaseHeap.resolve(addr) if isinstance(addr, tuple) else addr]
        (left, li), (right, ri) = self.get_children(ci)
        gleft = current is not None and left is not None and left > current
        gright = current is not None and right is not None and right > current
        while gleft or gright:
            if gleft and gright:
                if max(right, left) == right:  # type: ignore
                    gleft = False
                else:
                    gright = False

            if gleft:
                self.array[ci], self.array[ci := li] = left, current
            else:
                self.array[ci], self.array[ci := ri] = right, current

            current = self.array[ci]
            (left, li), (right, ri) = self.get_children(ci)
            gleft = current is not None and left is not None and left > current
            gright = current is not None and right is not None and right > current
```
## Graphs
- set of vertices & edges
### Edge
- connection between vertices
### Vertex
- unique point, destination or identifier inside a graph
- duplication of content is possible, but their identity remains unique
### Neighbor
- vertices connected directly by edges
### Degree of vertex
- number of edges connected to the vertex
### Path
- sequence of vertices connected by edges
### Path length
- number of edges in a path
### Cycle
- path that starts & ends at the same vertex
### Connected vertices
- at least one path exists between them
### Connected graph
- all of its vertices are connected
### Connected component
- subset of vertices of a graph which are connected
### Directed graph
- its edges are unidirectional
### Undirected graph
- its edges are bidirectional
### Cyclic graph
- contains cycles
### Acyclic graph
- doesn't contain cycles
### Weight
- attribute of edges
- represent different properties in different contexts
### Trees
- connected & acyclic graphs
    - broken if an edge is removed
    - cyclic end if an edge is added
### Representation
#### Adjacency list
- array whose indices associate with vertices & store edges of their corresponding vertices
- hash maps can be used if graph identifiers aren't contiguous
#### Adjacency matrix
- 2d matrix with rows & columns corresponding to each vertex
- entries are considered as edges
- applicable to finite graphs
### Graph BFS implementation
#### Using Adjacency list
```py
from queue import Queue

from graph import AdjGraphList, ListVertex


def list_breadth_first[T: ListVertex](graph: AdjGraphList[T], start: T | None = None) -> list[T]:
    q: Queue[T] = Queue()
    q.put(vrtx := start if start is not None else sorted(graph.keys())[0])
    bfs: list[T] = [vrtx]

    while not q.empty():
        for edge in graph[q.get()]:
            if (neighbor := edge[0]) not in bfs:
                bfs.append(neighbor)
                q.put(neighbor)

    return bfs
```
#### Using Adjacency matrix
```py
from queue import Queue

from graph import AdjGraphMatrix, MatrixVertex


def matrix_breadth_first(graph: AdjGraphMatrix, start: MatrixVertex = 0) -> list[MatrixVertex]:
    q: Queue[int] = Queue()
    q.put(start)
    bfs: list[MatrixVertex] = [start]

    while not q.empty():
        for v, w in enumerate(graph[q.get()]):
            if w != 0 and v not in bfs:
                bfs.append(v)
                q.put(v)

    return bfs
```

## Modules
### Linked list single link node
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, previous: Node[T] | None = None) -> None:
        self.value = value
        self.prev = previous
```
### Linked list double link node
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, previous: Node[T] | None = None, next: Node[T] | None = None) -> None:
        self.value = value
        self.next = next
        self.prev = previous
```
### Binary tree node
```py
from __future__ import annotations


class Node[T]:
    def __init__(self, value: T, *, left: Node[T] | None = None, right: Node[T] | None = None) -> None:
        self.value = value
        self.left = left
        self.right = right

```
### Fake array
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
```
### Base heap
```py
from typing import Literal

from arraylist import ArrayList
from btnode import Node

type Direction = Literal["l"] | Literal["r"] | Literal["u"]
type Path = tuple[Direction, ...]
type NodeID = Path | int
type NodeIDPair[T] = tuple[T | None, int]


class BaseHeap[T]:
    def __init__(self, height_capacity: int) -> None:
        self.array: ArrayList[T] = ArrayList(height_capacity**2)
        self.length = -1

    def push(self, value: T) -> None:
        self.array.append(value)
        self.length += 1
        self.heapify_up(self.length)

    def pop(self) -> T | None:
        out = self.array[0]

        self.array[0] = self.array[self.length]
        self.array[self.length] = None
        self.length -= 1

        self.heapify_down(0)

        return out

    def heapify_down(self, addr: NodeID) -> None:
        raise NotImplementedError

    def heapify_up(self, addr: NodeID) -> None:
        raise NotImplementedError

    def get_children(self, addr: NodeID) -> tuple[NodeIDPair[T], NodeIDPair[T]]:
        index = BaseHeap.resolve(addr) if isinstance(addr, tuple) else addr
        li, ri = BaseHeap.get_left(index), BaseHeap.get_right(index)

        try:
            right = self.array[ri]
        except IndexError:
            right = None

        try:
            left = self.array[li]
        except IndexError:
            left = None

        return ((left, li), (right, ri))

    def to_btnode(self, index: int = 0) -> Node[T] | None:
        if (val := self.array[index]) is None:
            return None
        else:
            node = Node(val)

        try:
            if self.array[left := BaseHeap.get_left(index)] is not None:
                node.left = self.to_btnode(left)
        except IndexError:
            pass

        try:
            if self.array[right := BaseHeap.get_right(index)] is not None:
                node.right = self.to_btnode(right)
        except IndexError:
            pass

        return node

    def __getitem__(self, path: Path) -> T | None:
        try:
            return self.array[BaseHeap.resolve(path)]
        except IndexError:
            return None

    @staticmethod
    def resolve(path: Path) -> int:
        needle = 0
        for dir_ in path:
            needle = (
                BaseHeap.get_left(needle)
                if dir_ == "l"
                else BaseHeap.get_right(needle) if dir_ == "r" else BaseHeap.get_up(needle)
            )
        return needle

    @staticmethod
    def get_right(index: int) -> int:
        return index * 2 + 2

    @staticmethod
    def get_left(index: int) -> int:
        return index * 2 + 1

    @staticmethod
    def get_up(index: int) -> int:
        return (index - 1) // 2
```
### Graph
```py
type Weight = int

type ListVertex = int | float | str
type ListEdge[T: ListVertex] = tuple[T, Weight]
type AdjGraphList[T: ListVertex] = dict[T, set[ListEdge[T]]]

type MatrixVertex = int
type AdjGraphMatrix = list[list[Weight]]
```