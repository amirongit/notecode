# Design Patterns In Object Oriented Programming

- [source](https://youtube.com/playlist?list=PLrhzvIcii6GNjpARdnO4ueTUAVR9eMBpc)

## Strategy
strategy pattern can be used to make interchangeable & unify similar algorithms which differ internally.<br>
each algorithm is implemented behind a shared interface exposing the desired behaviour.<br>
implementations of this interface are called strategies.<br>
clients will have attributes holding an implementaion of this interface & their requests will be delegated to the associated strategy.

it is useful when there is more than one way to do something.<br>
inheritance isn't preferred because it can lead to duplication on child classes sharing the same algorithm.<br>
strategy pattern is used to share behaviour horizontally.
## Observer
observer pattern defines a one to many dependency between the observable & observer objects.<br>
the observable implements a mechanism for observers to register callbacks & calls them upon certain events.

delegating the responsibility for querying the observable's state to the observer objects isn't preferred because of its pull based structure; this could lead to
- complicated decision making logic about when to query
- possibility of undesired delays
- large number of pointless function calls
## Decorator
decorator pattern is a solution to dynamically attach additional responsibilities to objects (at runtime).<br>
wrappers with the same interface as the decorated objects are created holding a reference to an instance.<br>
they delegate calls to the wrapped object & have the ability to modify inputs or outputs, thus, changing their behaviour.<br>
wrappers & the objects they wrap can be considered the same & be decorated again.

implementation of all possible variations in the original object isn't preferred because it would lead to fragile code.<br>
inheritance is also not preferred because it would lead to
- subclass explosion, since every modification can be combined with every other one
- difficulty of dynamically modifying the behaviour of the original object at runtime
## Factory method
factory method pattern defines an interface for creating single objects, letting its implementations decide
- which subtype of the object is created
- how & what arguments are computed & passed to the object's constructor

it is used when creating a dependency is complex, for example
- its specific type is determined at runtime
- there is more than one way to wire up & instantiate it
## Abstract factory
abstract factory pattern defines an interface with multiple factory methods for creating families of dependent or related objects, letting its implementations
- decide which subtype of each object is created
- encapsulate each family of objects
## Singleton
singleton pattern ensures that a class has only one instance & provides a global point of access to it.
## Command
command pattern encapsulates requests (& optionally their inverse logic) into units of behaviour.<br>
units are called commands & can be used to parameterize other objects; objects which trigger commands are usually called invokers.<br>
commands hold references to their dependencies internally & implement an interface exposing their execution & optionally its inverse.<br>
objects which commands operate on are called receivers; command pattern is agnostic about receivers & invokers.<br>
it is also possible to implement macros using this pattern, merging multiple commands into a single one.
## Adapter
adapter pattern converts the interface of an object into another interface by wrapping it.<br>
it is used to let clients depend on stable internal (or predefined) interfaces, avoiding modifications & allowing interactions between incompatible objects.<br>
## Facade
facade pattern provides a high level unified interface to a set of interfaces in a subsystem in order to make it easier to use.
## Proxy
proxy pattern provides a place holder for another object in order to control access to it.<br>
place holders expose the same interface that the object they are wrapping does; they just intercept.<br>
there are three types of proxies
1. remote: used to communicate with out of process dependencies
2. virtual: used to implement caching mechanisms, lazy computations, etc... on expensive dependencies
3. protection: used to enforce access rights on sensetive dependencies
## Bridge
terminology
- domain abstraction (aka abstraction): client facing high level interface
- refined abstraction: specialized version of domain abstraction
- implementor (aka implementation): low level interface defining operations relied on by abstractions
- implementation (aka concrete implementation): implements operations defined by its implementor

bridge pattern decouples abstractions from implementors so that they can vary independently.<br>
it introduces composition over inheritance to avoid class explosions from combining every abstraction & implementation.
