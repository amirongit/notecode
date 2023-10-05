# Coroutines

## Implementation

It is possible to implement coroutines using generators (althogh coroutines have
their own syntax). PEP 492 introduced native coroutines & separated them from
generators.\

### syntax

Native coroutines are declared using "async def" syntax. The "await" keyword,
suspends the execution of the coroutine untill the awitable completes. This
happens in a generator based coroutine by yield.\
The argument passed to await should be a native coroutine, a generator based
coroutine decorated with types.coroutine or an object with "__await__" method
implemented on it (which is also called a future object).\n
Asynchronous context managers can suspend execution in their enter & exit
methods. They must be used inside coroutines only & implement aenter & aexit
methods. This is the same for asynchronous iterables & iterators.

## David Beazley's videos on coroutines

- watch theme [here](https://youtube.com/playlist?list=PLYGzOXYlwaA-4ML9coZ2cTTnaRDWt7pyc&si=UVPYSAQxI1pgG9Jp)

Coroutines & generators better be considered as two separate concepts. In the
context of generators, the callable produces values. So if multiple generators
are chained together, values would be pulled of the pipeline. But int the
context of coroutines which are consumers, values would be pushed to the
pipeline instead.\n
Considering the flow of the data in the coroutine chain, there is the ability
to branch out the flow and send data to multiple or one another future coroutine.
