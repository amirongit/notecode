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
|london take|modules|single classes or methods|mutable dependencies (whose internal state changes their external behaviour)|
|detroit take|test cases|behaviour|shared dependencies|
#### How The Classical & London Schools Handle Dependencies
- value objects
    - also called values
    - have no individual identity
    - identified by their content
    - interchangeable with other objects containing similar content
- shared or mutable dependencies are also called collaborators
### Contrasting The Classical & London Schools Of Unit Testing
- benefits of the london school
    - better granularity
    - easier to test complicated graphs of interconnected modules
    - failures usally point directly to where the problem lies
#### Unit Testing One Class At A Time
<!--
    heavily opinionated, page 35
    meaningless classes (& other objections towards the london school in the following paragraphs)
    are signs of shitty code, which can't be resolved by merely thinking about tests.
-->
> tests should tell stories about the domain, thus, they should be cohesive & meaningful to non programmers
- unit tests should verify units of behaviour rather than units of code
- number of classes (or modules) it takes to implement behaviours is irrelevant
- it is hard to tell what exactly unit tests verify if they exercise things less than units of behaviour
### Integration Tests In The Two Schools
- for the london school, integration tests use real collaborators
- for the classical school, side effects of integration tests aren't isolated
## The Anatomy Of A Unit Test
### How To Structure A Unit Test
#### Using The 3A Pattern
- unit tests are splitted into 3 parts (aka "given, when, then" pattern among non technical people)
- arrange (given): bringing the system to desired state
- act (when): invoking the system using prepared dependencies in the arrange phase & capturing its output
- assert (then): verify the outcome which might include
    - comparing values
    - verifying state of the system itself
    - verifying state of collaborators
    - verifying methods of collaborators being invoked by the system
#### Avoid Multiple 3A sections
- this indicates verification of multiple units
#### Avoid If Statements In Tests
- this indicates either verification of too many things at once or non deterministic behaviours of domain code
- this is an anti pattern which increases maintenance cost of test code
#### How Large Should Each Section Be?
> the act of protecting your code against potential inconsistencies is called encapsulation
- arrange
    - doesn't matter
    - [object mother](https://martinfowler.com/bliki/ObjectMother.html) & test data builder patterns could be used to make it more compact
- act
    - usually should be one line of could which invokes the system
    - having to do more increases the possibility of state inconsistency & indicates lack of encapsulation
### Reusing Test Fixtures Between Tests
- fixture
    - used to reduce "arrange" phase related code
    - regular dependency of system under test or some data
    - needs to be in one single known state before each test, hence the term fixture
#### High Coupling Between Tests Is An Anti Pattern
> modification of one test should not affect other tests
- shared states used as arrangement will cause common assumptions between tests (coupling)
<!--
    but fixtures are "fixed" & should be allowed as common assumptions because shall not change!
-->
#### The Use Of Constructors In Tests Diminishes Test Readability
- extracting arrangement code out of test cases makes them less readable by moving assumptions somewhere else
#### A Better Way To Reuse Test Fixtures
- using private factory methods
    - shortens arrangement code without coupling or removing context
    - allows more flexibality & reusabality
### Refactoring To Parameterized Tests
- parameterized tests allow providing arguments for unit tests
- unit tests having common 3A phases with different values can be grouped together using this feature
- parameterized tests allow capturing different branches behind the unit in one single test
- there is trade off between readability & the amount of test code here
<!-- page 65 -->
