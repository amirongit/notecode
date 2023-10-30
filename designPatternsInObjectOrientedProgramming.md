# Design Patterns In Object Oriented Programming

## Strategy pattern

### the problem

- there are more than one way to do something
- inheritance can't be used
  - may cause duplication on classes that share the same algorithm which is
not the parents
  - inheritance shares behaviours vertically in a hirearchy; therefore it isn't
a solution to share behaviours horizontally
- putting all the algorithms in the same class could cause it to become big and
hard to maintain; also, the clients which just want the behaviours, will have to
know about the implementation details.

### the solution

- algorithms should all implement a single interface which exposes the
desired behaviour (implementations are called strategies)
- the class should have an attribute dedicated to an instance of the
mentioned interface
- objects of the class are configured in constructors to have the desired
strategy
- clients requests for the behaviour will be delegated by the class to the
associated strategy
