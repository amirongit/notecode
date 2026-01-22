<!--
    Dependency Injection: Principles, Practices, Patterns
    Algebraic Data Types
    http://mng.bz/KE9O
-->
# Unit Testing: Principles, Practices & Patterns
## The Goal Of Unit Testing
### The Goal Of Unit Testing
- keeping reasonable ratio between coding or debugging time & adding or modifying features (sustainability & scalability)
#### What Makes A Good Or Bad Test?
- test code also has maintenance cost
### Using Coverage Metrics To Measure Test Suite Quality
- coverage is good negative & bad positive indicator tool
#### Understanding The Code Coverage Metric
- ratio between lines exercised by test suite & all of code
- easy to manipulate by making code more compact  (using inline syntaxes, etc...)
- aka test coverage (?)
#### Understanding The Branch Coverage Metric
- ratio between lines exercised by test suite & all branches of code
- focused on flow control structures
#### Problems With Coverage Metrics
- test suite quality can't be determined by coverage metrics
- code coverage exercises code but doesn't verify results (it is done by assertions)
- branch coverage ignores paths of external libraries (?)
#### Aiming At A Particular Coverage Number
- coverage metrics are indicators, not goals in & of themselves
### What Makes A Successfull Test Suite?
- integrated into development cycle (continuously run after code changes)
- targets only most important parts of code
- provides maximum value with minimum maintenance cost
#### It Targets Only The Most Important Parts Of Your Code Base
- not all parts of code is important
- unit tests should verify important parts of code (usually the domain model)
- non critical code should be verified briefly or indirectly
    - infrastructure
    - third party
    - wireup
#### It Provides Maximum Value With Minimum Maintenance Costs
- writing valuable unit test isn't possible without properly structured & written code
## What Is A Unit Test?
### The Definition Of "unit test"
- essential attributes among most definitions
    - verifies small piece of code (unit)
    - executed automatically & quickly
    - comes as isolated unit test cases
#### The Isolation Issue: The London Take
- isolates modules under test from their collaborators by injecting or monkey patching [test double](https://martinfowler.com/bliki/TestDouble.html)s
- defines units as capsules of limited data & behaviour
- reduces external influence on the unit when it is being tested
- separates behaviour from external state which makes it precise & direct
- splits object graph which reduces the amount of preparation in test code
- asserts against modules & their interactions with their collaborators
#### The Isolation Issue: The Detroit Take
- isolates tests & their side effects rather than modules
- defines units as behaviour (which could be spread across multiple modules)
- types of dependencies
    - out of process
        - runs outside the application's execution process
        - calls to these dependencies violates the "quick" attribute of unit tests
    - shared
        - provides means for tests to affect each other's outcome
        - usually an static mutable field accessible by all unit tests
    - private:
        - is not shared between unit tests
        - usually in memory
    - volatile:
        - may require runtime environment setup like databases & 3rd party APIs
        - may contain non deterministic behaviour
- asserts against state of system
### The Classical & London Schools Of Unit Testing
|school|isolation of|units are|test doubles used for|
|-|-|-|-|
|london take|units|single classes or methods|mutable dependencies|
|detroit take|unit tests|depends!|shared dependencies|

- mutable dependencies whose internal state changes their external behaviour
#### How The Classical & London Schools Handle Dependencies
- value object
    - also called value
    - has no individual identity
    - identified by its content
    - interchangeable with another object containing the same content
    - considered as immutable & private dependency
- shared or mutable dependencies are also called collaborators
### Contrasting The Classical & London Schools Of Unit Testing
- benefits of the london school
    - better granularity
    - easier to test complicated graphs of interconnected modules
    - failures usally point directly to where the problem lies
#### Unit Testing One Class At A Time
<!--
    heavily opinionated, page 35
    meaningless classes (& other objections towards the classical school in the following paragraphs)
    are signs of shitty code, which can't be resolved by merely thinking about tests.
-->
> tests should tell stories about the domain, thus, they should be cohesive & meaningful to non programmers
- unit tests should verify units of behaviour rather than units of code
- number of classes (or modules) it takes to implement behaviours is irrelevant
- it is hard to tell what exactly unit tests verify if they exercise things less than units of behaviour
### Integration Tests In The Two Schools
- for the london school, integration tests use real collaborators
- for the classical school, side effects of integration tests aren't isolated
<!-- 41 -->
