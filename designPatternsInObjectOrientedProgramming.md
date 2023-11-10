# Design Patterns In Object Oriented Programming

## Strategy pattern

### the problem

- there are more than one way to do something
- inheritance can't be used
  - may cause duplication on classes that share the same algorithm which is not the parents
  - shares parent's behaviour vertically in a hirearchy; therefore it isn't a solution to share behaviours horizontally
- putting all the algorithms in the same class could cause it to become big and
hard to maintain; also, the clients which just want the behaviours, will have to know about the implementation details.

### the solution

- algorithms should all implement a single interface which exposes the desired behaviour (implementations are called strategies)
- the class should have an attribute dedicated to an instance of the mentioned interface
- objects of the class are configured in constructors to have the desired strategy
- clients requests for the behaviour will be delegated by the class to the associated strategy

## Observer pattern

### the problem

- there are some objects interested in the internal state of an object and it's changes
- interested objects can't ask the object
  - it's complicated to decide when to ask
  - it is possible to have undesired delays
  - it would make a lot of pointless function calls

### the solution

- the object who's internal changes are being interested in by other objects should take the responsibality to notify them
- by doing this, polling mechanisms which are heavy & in efficient would be replaced by a pushing mechanism which is exteremely more efficient
- observers are registered on the observable (it's a one to many relationship)
- the subject (or observable) keeps track of it's observers and notifys theme on changes
