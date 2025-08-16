# Coroutines

## Implementation

It is possible to implement coroutines using generators (althogh coroutines have
their own syntax). PEP 492 introduced native coroutines & separated them from
generators.

### About the syntax

Native coroutines are declared using `async def` syntax. The `await` keyword
suspends the execution of the coroutine untill the awitable completes. This
happens in a generator based coroutine by yield.\
The argument passed to await should be a native coroutine, a generator based
coroutine decorated with types.coroutine or an object with `__await__` method
implemented on it (which is also called a future object).\
Asynchronous context managers can suspend execution in their enter & exit
methods. They must be used inside coroutines only & implement aenter & aexit
methods. This is the same for asynchronous iterables & iterators.

## Curious course on coroutines and concurrency

- [source](https://youtu.be/Z_OAlIhXziw?si=Q5__IHpvkUMJYInt)

### Introduction to coroutines, pipelines & data flow

Coroutines & generators better be considered as two separate concepts. In the
context of generators, the function produces values.\
So if multiple generators are chained together, values would be pulled out of the
pipeline with iteration. On the other hand, coroutines which are consumers, push
values into the pipeline via `send` instead.\
Considering the flow of the data in a coroutine pipeline, one has the ability
to branch out the flow & send data to multiple or one another coroutine.

### Coroutines & event dispatching

`yield` can be used in such a way to let the outside code alter the control flow
of the function; Considering this, one has the ability to build a state machines
on top of the concpet of coroutines which switches between different states upon
received values & handles them.

### Coroutines as tasks

In concurrent programming, one typically subdivides problems into tasks; The
essential features of tasks would be:

- independent control flow
- schedulability
- internal state
- communication with other tasks

all of which are provided by coroutines.

### Task scheduling

For a CPU, a program is just a series of instructions & there is not really a
notion of doing more than one thing at a time or any kind of task switching.\
So considering the fact that neither CPUs nor the programs know about
multitasking, how it happens? Well, ofcourse it should be the OS which does
that; But how does an operating system which is not running suspend a task
which is?\
There are usually two mechanisms that an oeprating system uses to gain control:

- interrupts (hardware generated event signals)
- traps (software generated request signals)

In either cases, the CPU briefly suspends the task & runs OS code. It is at that
point in time which the operating system takse control and has the ability to
switch tasks after handling the request or the event.

```
task y    --->REQ                       --->REQ...
                 \                     /
REQ / EVN         OS--->         OS--->
                        \       /
task z                   --->EVN
```

If `yield`s are treated as traps, it is possible to write a an oeprating system
(well, let's just call it a task scheduler!) in python.
