# Design Patterns in Object Oriented Programming
- [source](https://youtube.com/playlist?list=PLrhzvIcii6GNjpARdnO4ueTUAVR9eMBpc)
## Strategy
the strategy pattern can be used to make interchangeable and unify similar algorithms that differ internally.<br>
each algorithm is implemented behind a shared interface exposing the desired behavior.<br>
implementations of this interface are called strategies.<br>
clients will have attributes holding an implementation of this interface, and their requests will be delegated to the associated strategy.

it is useful when there is more than one way to do something.<br>
inheritance isn't preferred because it can lead to duplication on child classes sharing the same algorithm.<br>
the strategy pattern is used to share behavior horizontally.
## Observer
the observer pattern defines a one to many dependency between the observable and observer objects.<br>
the observable implements a mechanism for observers to register callbacks and calls them upon certain events.

delegating the responsibility for querying the observable's state to the observer objects isn't preferred because of its pull based structure; this could lead to
- complicated decision making logic about when to query
- the possibility of undesired delays
- a large number of pointless function calls
## Decorator
the decorator pattern is a solution to dynamically attach additional responsibilities to objects at runtime.<br>
wrappers with the same interface as the decorated objects are created, holding a reference to an instance.<br>
they delegate calls to the wrapped object and have the ability to modify inputs or outputs, thus changing their behavior.<br>
wrappers and the objects they wrap can be considered the same and be decorated again.

implementation of all possible variations in the original object isn't preferred because it would lead to fragile code.<br>
inheritance is also not preferred because it would lead to
- subclass explosion, since every modification can be combined with every other one
- difficulty dynamically modifying the behavior of the original object at runtime
## Factory Method
the factory method pattern defines an interface for creating single objects, letting its implementations decide
- which subtype of the object is created
- how and what arguments are computed and passed to the object's constructor

it is used when creating a dependency is complex, for example
- its specific type is determined at runtime
- there is more than one way to wire up and instantiate it
## Abstract Factory
the abstract factory pattern defines an interface with multiple factory methods for creating families of dependent or related objects, letting its implementations
- decide which subtype of each object is created
- encapsulate each family of objects
## Singleton
the singleton pattern ensures that a class has only one instance and provides a global point of access to it.
## Command
the command pattern encapsulates requests, and optionally their inverse logic, into units of behavior.<br>
units are called commands and can be used to parameterize other objects; objects which trigger commands are usually called invokers.<br>
commands hold references to their dependencies internally and implement an interface exposing their execution and, optionally, its inverse.<br>
objects which commands operate on are called receivers; the command pattern is agnostic about receivers and invokers.<br>
it is also possible to implement macros using this pattern, merging multiple commands into a single one.
## Adapter
the adapter pattern converts the interface of an object into another interface by wrapping it.<br>
it is used to let clients depend on stable internal or predefined interfaces, avoiding modifications and allowing interactions between incompatible objects.
## Facade
the facade pattern provides a high level unified interface to a set of interfaces in a subsystem in order to make it easier to use.
## Proxy
the proxy pattern provides a place holder for another object in order to control access to it.<br>
place holders expose the same interface that the object they are wrapping does; they just intercept.<br>
there are three types of proxies
1. remote: used to communicate with out of process dependencies
2. virtual: used to implement caching mechanisms, lazy computations, etc. on expensive dependencies
3. protection: used to enforce access rights on sensitive dependencies
## Bridge
the bridge pattern decouples abstractions from implementors so that they can vary independently
- domain abstraction (aka abstraction): client facing high level interface
- refined abstraction: specialized version of domain abstraction
- implementor (aka implementation): low level interface defining operations relied on by abstractions
- implementation (aka concrete implementation): implements operations defined by its implementor

it introduces composition over inheritance to avoid class explosions from combining every abstraction and implementation.
## Template Method
template method pattern defines the skeleton of an algorithm, deferring specific steps to its subclasses.<br>
it lets subclasses redefine certain steps of the algorithm without changing its structure.
## Composite
composite pattern composes objects of the same interface into tree-like hierarchies so that individual objects & their composition expose the same interface.<br>
it lets clients treat leaf & container nodes uniformly.
## Iterator
iterator pattern provides a mechanism to access items of an aggregate object sequentially, without exposing its underlying representation.<br>
it allows different aggregate objects having their own implementations to be iterated over using the same mechanism.
## State
state pattern is built upon the concept of [state machine](https://en.wikipedia.org/wiki/Finite-state_machine)s.<br>
it allows objects to alter their behavior when their internal state changes
- context: object whose behavior varies depending on its internal state, usually keeps a reference to its current state object
- state: object that implements a common interface with other states & handles operations in a state-specific way
