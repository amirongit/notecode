# Design Patterns In Object Oriented Programming

## Strategy

### problem

- there are more than one way to do something
- inheritance can't be used
  - may cause duplication on classes that share the same algorithm which is not the parents
  - shares parent's behaviour vertically in a hirearchy; therefore it isn't a solution to share behaviours horizontally
- putting all the algorithms in the same class makes it big & hard to maintain & the clients will have to know the implementation details

### solution

- algorithms should all implement a single interface which exposes the desired behaviour (implementations are called strategies)
- the class should have an attribute dedicated to an instance of the mentioned interface
- objects of the class are configured in constructors to have the desired strategy
- clients requests for the behaviour will be delegated by the class to the associated strategy

## Observer

### problem

- there are some objects interested in the internal state of an object & it's changes
- interested objects can't ask the object
  - it is complicated to decide when to ask
  - it is possible to have undesired delays
  - it would make a lot of pointless function calls

### solution

- the object who's internal changes are being interested in by other objects should take the responsibality to notify them
- by doing this heavy & inefficient polling mechanisms would be replaced by an efficient pushing mechanism
- observers are registered on the observable (it's a one to many relationship)
- the subject (or observable) keeps track of it's observers & notifys theme on changes

## Decorator

### problem

- there are many possible modifications to apply on behaviours
  - making all possible combinations of behaviours & modifications leads to subclass explosion which makes code hard to maintain
- it is required to modify or compose behaviours dynamically in runtime

### solution

- a wrapper is created with the same interface which the behaviour being modified implements
- the wrapper delegates calls to the behaviour it wraps & modifies the result before or after calling
- now the wrappers & the objects being wrapped are considered the same & can be passed to other wrappers in runtime

## Factory method

### problem

- instantiation of a dependency could be complex; for example, provided parameters could be changed in runtime
- the specific implementation of an interface is meant to be determined in runtime
- more than one approache exists or is required to wire up & instantiate dependencies

### solution

- the logic behind the instantiation & configuration of dependencies is encapsulated in different factory objects / classes which implement the same factory interface
- implementations of the factory interface have the ability to choose between different subclasses of a particular dependency & implement their own way of constructing them

## Abstract factory

### problem

- a sensible set of related instances of dependencies are needed to be created without pointing to an specific implementation of them

### solution

- an interface is designed to instantiate each one of the dependencies with a factory method
- each set of dependencies could be encapsulated in an implementation of this interface
