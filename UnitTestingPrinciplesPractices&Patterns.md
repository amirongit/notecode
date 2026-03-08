<!--
    Dependency Injection: Principles, Practices, Patterns
    Algebraic Data Types
    http://mng.bz/KE9O
    https://martinfowler.com/bliki/TellDontAsk.html
    https://enterprisecraftsmanship.com/posts/ocp-vs-yagni
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
#### Understanding The Branch Coverage Metric
- ratio between lines exercised by test suite & all branches of code
- focused on flow control structures
#### Problems With Coverage Metrics
- test suite quality can't be determined by coverage metrics
- code coverage exercises code but doesn't verify results (it is done by assertions)
- branch coverage ignores paths of external libraries (they don't need to be tested though?!)
#### Aiming At A Particular Coverage Number
- coverage metrics are indicators, not goals in & of themselves
### What Makes A Successfull Test Suite?
- integrated into development cycle (continuously run after code changes)
- targets only most important parts of code
- provides maximum value with minimum maintenance cost
#### It Targets Only The Most Important Parts Of Your Code Base
- not all parts of code is important
- unit tests should verify important parts of code (usually domain model)
- non critical code should be verified briefly or indirectly
    - infrastructure
    - third party
    - wireup
#### It Provides Maximum Value With Minimum Maintenance Costs
- writing valuable unit test isn't possible without properly structured & written code
## What Is A Unit Test?
### The Definition Of Unit Test
- essential attributes among most definitions
    - verifies small piece of code (unit)
    - executed automatically & quickly
    - comes as isolated unit test cases
#### The Isolation Issue: The London Take
- isolates modules under test from their collaborators by injecting or monkey patching [test double](https://martinfowler.com/bliki/TestDouble.html)s
- defines units as capsules of limited data & behaviour
- reduces external influence on the unit when it is being tested
- separates behaviour from external state which makes it precise & direct
- splits object graph which reduces amount of preparation in test code
- asserts against modules & their interactions with their collaborators
#### The Isolation Issue: The Detroit Take
- isolates tests & their side effects rather than modules
- defines units as behaviour (which could be spread across multiple modules)
- types of dependencies
    - out of process
        - runs outside the application's execution process
        - calls to these dependencies violates the quick attribute of unit tests
    - shared
        - provides means for tests to affect each other's outcome
        - usually an static mutable field accessible by all unit tests
    - private
        - isn't shared between unit tests
        - usually in memory
    - volatile
        - may require runtime environment setup like databases & 3rd party APIs
        - may contain non deterministic behaviour
- asserts against state of system
### The Classical & London Schools Of Unit Testing
|school|isolation of|units are|test doubles used for|
|-|-|-|-|
|london take|units|single classes or methods|mutable dependencies (whose internal state changes their external behaviour)|
|detroit take|unit test cases|behaviour spread across classes or methods|shared dependencies|
#### How The Classical & London Schools Handle Dependencies
- value objects
    - also called values
    - have no individual identity
    - identified by their content
    - interchangeable with other objects containing similar content
- shared or mutable dependencies are also called collaborators
### Contrasting The Classical & London Schools Of Unit Testing
- benefits of london school
    - better granularity
    - easier to test complicated graphs of interconnected modules
    - failures usally point directly to where problems lie
#### Unit Testing One Class At A Time
<!--
    heavily opinionated, page 35
    meaningless classes (& other objections towards london school in the following paragraphs)
    are signs of shitty code, which can't be resolved by merely thinking about tests.
-->
- tests should tell stories about domain & be cohesive & meaningful to non programmers
- unit tests should verify units of behaviour rather than units of code
- number of classes (or modules) it takes to implement behaviours is irrelevant
- it is hard to tell what exactly unit tests verify if they exercise things less than units of behaviour
### Integration Tests In The Two Schools
- for london school, integration tests use real collaborators
- for classical school, side effects of integration tests aren't isolated
## The Anatomy Of A Unit Test
### How To Structure A Unit Test
#### Using The 3A Pattern
- unit tests are splitted into 3 parts (aka given, when, then pattern among non technical people)
- arrange (given): bringing system to desired state
- act (when): invoking system using prepared dependencies in arrange phase & capturing its output
- assert (then): verify the outcome which might include
    - values
    - state of system itself
    - state of collaborators
    - methods of collaborators being invoked by the system
#### Avoid Multiple 3A sections
- this indicates verification of multiple units
#### Avoid If Statements In Tests
- this indicates either verification of too many things at once or non deterministic behaviours of domain code
- this is an anti pattern which increases maintenance cost of test code
#### How Large Should Each Section Be?
- the act of protecting your code against potential inconsistencies (invariant violations) is called encapsulation
- invariants are conditions which shall hold true at all times
- arrange
    - doesn't matter
    - [object mother](https://martinfowler.com/bliki/ObjectMother.html) & test data builder patterns could be used to make it more compact
- act
    - usually should be one line of could which invokes the system
    - having to do more increases the possibility of state inconsistency & indicates lack of encapsulation
### Reusing Test Fixtures Between Tests
- fixture
    - used to reduce arrange phase related code
    - regular dependency of SUT or some data
    - needs to be in one single known state before each test, hence the term fixture
#### High Coupling Between Tests Is An Anti Pattern
- modification of one test should not affect other tests
- shared states used as arrangement will cause common assumptions between tests (coupling)
<!--
    but fixtures are fixed & should be allowed as common assumptions because they shall not change!
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
- there is trade off between readability & amount of test code here
## The Four Pillars Of A Good Unit Test
### Diving Into The Four Pillars Of A Good Unit Test
1. protection against regressions
2. resistance to refactoring
3. fast feedback
4. maintainability
#### The First Pillar: Protection Against Regressions
- regression is when features stop working after certain events such as refactoring or adding features
- amount of regression potential is related to amount of code
- evaluation factors
    - amount of exercised code (with proper assertions)
    - complexity of exercised code
    - domain significance of exercised code
#### The Second Pillar: Resistance To Refactoring
- refactoring means to change existing code without modifying its observable behaviour
- false positives are test failures caused by refactoring (while SUT is healthy & correct)
- degree to which tests are able to sustain refactoring of SUT withou failing
- tests make growth of code sustainable by allowing safe & regular refactoring & development of features
- false positives punish refactoring & allow real problems slip into production environment, removing value of test suites
#### What Causes False Positives
- solution to false positives is to decouple test cases from implementation details
- test cases shall treat SUT from the POV of its real client
- verifying only end results (observable behaviours), not steps taken to produce them (implementation or algorithm)
### The Intrinsic Connection Between The First Two Attributes
#### Maximizing Test Accuracy
|test result|functional validity|inference|solution|
|-|-|-|-|
|pass|correct|true negative|-|
|pass|incorrect|false negative|[protection against regression](#the-first-pillar-protection-against-regressions)|
|fail|incorrect|true positive|-|
|fail|correct|false positive|[resistance to refactoring](#the-second-pillar-resistance-to-refactoring)|
### The Third & Fourth Pillars: Fast Feedback & Maintainability
- fast feedback
    - cost of fixing bugs is related to the time it took for them to be noticed
    - slow running test cases avoid bugs to be noticed which allows moving forward in wrong direction
- maintainability
    - readability & size of test cases
    - ease of execution
### Exploring Well Known Test Automation Concepts
- protection against regression, fast feedback & resistance to refactoring are mutually exclusive
- one single test case is capable of only emphasize two out of these three attributes
- resistance to refactoring is usually either true or false
- this will make the trade off only exist between fast feedback & resistance to refactoring
#### Breaking Down The Test Pyramid
- advocates for certain ratio of unit, integration & end to end tests
- test types in the pyramid make choices between fast feedback & protection against regression
    - end to end tests favor protection against regression (top)
    - integration tests lie in the middle (middle)
    - unit tests emphasize fast feedback (bottom)
#### Choosing Between Black Box & White Box Testing
- black box testing
    - aims at testing software without knowing its internal structure
    - usually built on specifications
    - focused on what rather than how
- white box testing
    - verifies inner workings of software
    - derived from source code rather than specifications
## Mocks & Test Fragility
### Differentiating Mocks From Stubs
#### The Types Of Test Doubles
- test double is an overarching term that describes all kinds of non production ready fake dependencies in tests
- passed as fake dependencies to systems under tests instead of real ones
- used when cost of passing real dependencies to the SUT is too heavy
- variations of test doubles
    - mocks: emulate & examin outgoing interactions (called by SUT to change state)
        - mock: made using already existing libraries
        - spy: hand written mocks
    - stubs: emulate incoming interactions (called by SUT to get input data)
        - dummy
            - its only job is to satisfy method signatures
            - may return hard coded & fakse values
            - doesn't participate in production of final outcome
        - stub: smart dependency configurable to return certain values in different situations
        - fake: same as stub, but implemented as replacement for dependencies not yet existing
#### Don't Assert Interactions With Stubs
- this is an anti pattern which leads to fragile tests
- mocks are used to examin outgoing interactions which are meaningful in domain model
- stubs are used to emulate incoming interactions which are implementation details
- assertion against implementation details is against resistance to refactoring attribute
- practice of verifying events that aren't part of end result is called overspecification
#### Using Mocks & Stubs Together
- stubs & mocks can be on one test double but within different methods
#### How Mocks & Stubs Relate To Commands & Queries
- CQS principle states that each method should either be command or query, but not both
- commands produce side effects without returning values
- queries are side effect free & return values
- mocks substitute commands
- stubs substitute queries
### Observable Behaviour vs. Implementation Details
- test fragility corresponds to resistance to refactoring attribute
#### Observable Behaviour Isn't The Same As Public API
- an operations is one method that calculates, incurs side effects or both
- code can be categorized into two dimensions
    1. public API vs. private API
    2. observable behaviour vs. implementation details
- these dimensions don't overlap, meaning that one piece of code belongs to either one of the categories, but not both
- observable behaviour is code that exposes either of these in order to directly help clients achieve specific goals
    - operations
    - state of system
- code exposing neither is considered as implementation detail
- ideally, public API & observable behaviour are together & coincide with each other
#### Leacking Implementation Details: An Example With An Operation
- ideally, any individual goal shall be achieved through one single operation
- otherwise, public API might be leaking implementation details
#### Well Designed API & Encapsulation
- exposing implementation details allows invariant violations by giving control of internal state to clients
- encapsulation reduces code complexity & the possibility of invariant violations by hiding internal state
<!-- complete after reading tell don't ask by martin fowler -->
#### Leaking Implementation Details: An Example With State
- making APIs well designed automatically improves unit tests
- absolute minimum amount of operations & state shall be exposed to clients (only the most direct ones)
- everything else shall be hidden from clients & considered as private state
- it isn't even possible to leak or hide observable behaviour because of its very definition
### The Relationship Between Mocks & Test Fragility
#### Defining Hexagonal Architecture
- hexagonal architecture emphasizes on three guidelines
    1. separation of concerns between the domain & application service layer
        - domain layer should be as isolated as possible (collection of how tos)
        - application service layer orchestrates domain layer, dependencies & clients in order to achieve goals (use cases) (collection of what tos)
    2. communications inside application
        - dependencies shall flow only from application service layer to domain layer
        - classes inside domain layer shall only depend on each other
    3. communications between applications
        - applications shall communicate through common interfaces maintained by & in application service layers
        - domain layer shall not be accessed directly
- each layer contains observable behaviours & implementation details
- test cases working on different layers could be verifying the same behaviours on different levels (or have overlaps)
- for domain layer, application service layer is client which for external client itself is considered as client
#### Intra System vs. Inter System Communications
- intra system
    - communications between components inside one application
    - not directly related to goals of clients
    - implementation detail
    - verification by test cases makes them fragile & falls short in resistance to refactoring attribute
    - can be replaced by stubs in test cases
- inter system
    - communications between multiple applications
    - considered as outcome or side effect which is part of end result
    - observable behaviour
    - shall be verified by test cases using mocks
    - communication protocols of this type are contracts (shared interfaces) with external clients
    - backward compatibality is important & refactoring shall not change the way or content of these type of communications
#### The Classical School vs. London School Of Unit Testing, Revisited
<!--
    but what if intra system communications happened also upon interfaces which mocks maintained?
    is that too much maintenance cost?
    but of course they won't be mocks anymore. they'll be another implementation of the mentioned interfaces.
-->
- london school advocates mocking all but immutable dependencies regardless of type of communications
- this will lead to test fragility by violating resistance to refactoring attribute by verifying implementation details
#### Not All Out Of Process Dependencies Should Be Mocked Out
- detroit school advocates avoiding shared dependencies to keep of executing unit tests in parallel through isolation of side effects possible
- shared & not out of process dependencies are easy to avoid being reused by providing new instances of them in each unit test
- shared out of process dependencies are usually replaced by test doubles, because its not practical to spawn processes per each unit test
- if such dependency is only accessible by one application, communications with it aren't part of observable behaviours
- need to protect backward compatibality & contracts doesn't exist for such dependency because of refactoring possibility
- using mocks for such dependencies violates resistance to refactoring attribute because of control the application has on such dependency
#### Using Mocks To Verify Behaviour
- only communications which can be traced back to client goals shall be verified
## Styles Of Unit Testing
### The Three Styles Of Unit Testing
- it is possible to employ more than one of these styles in one single unit test
- detroit school prefers state based style
- london school prefers communication based style
- output based style is preferred anyways & shall be employed solely when possible
#### Defining The Output Based Style
- feeds specific input to SUT & checks for specific outputs (aka functional)
- applicable to code which doesn't produce side effects (by mutating state), so only returned output needs to get checked
#### Defining The State Based Style
- verifies state of SUT or one of its dependencies after invoking some operation
#### Defining The Communication Based Style
- uses test doubles to verify communications between SUT & its dependencies
### Comparing The Three Styles Of Unit Testing
#### Comparing The Styles Using The Metrics Of Protection Against Regressions & Fast Feedback
- extreme cases of communication based style may violate protection against regressions attribute by exercising little amounts of code
- if no out of process dependencies is used by SUT, all styles score the same for fast feedback attribute
#### Comparing The Styles Using The Metric Of Resistance To Refactoring
- test cases of output based style are only coupled to SUT itself & its output, scoring highest
- state based test cases are more prone to false positives by also being coupled to state of SUT, covering larger API surface, scoring second best
- communication based test cases score lowest by being coupled to internal communications of SUT
#### Comparing The Styles Using The Metric Of Maintainability
- output based test cases score highest by having smaller 3A phases than other styles & not checking for any states
- state based test cases score second best by having large assertion phases which also may engage with out of process dependencies
- communication based test cases score lowest by having large arrange & assert phases which also may contain mock chains
#### Comparing The Styles: Test Results
- output based tests are the best! (:
- but this style of testing can only be applied on functional code (zero to non side effects & internal dependencies)
### Understanding Functional Architecture
#### What Is Functional Programming
- mathematical functions (aka pure functions)
    - don't have hidden inputs or outputs
    - all inputs & outputs are explicitly expressed method signatures
    - produce same output for same input regardless of time, states or present conditions (are deterministic)
    - match mathematical definition of functions: relation in which each unique first component corresponds to one non-unique second component
    - replaceable by values they return (aka referential transparency)
- programming with mathematical functions
- hidden inputs & outputs make code less testable & readable
    - side effects
    - exceptions
    - references to internal or external states: such as accessing current date & time or data stores (introducing non determinism)
#### What Is Functional Architecture?
- pushes side effects to edge of domain operations
- maximizes purely functional code & minimizes code that deals with side effects
- introduces separation between domain model & code that incurs side effects
    1. functional core (aka immutable core)
        - makes decisions
        - doesn't require side effects
        - can be implemented by mathematical functions
        - shall not depend on mutable shell
    2. mutable shell
        - acts upon decisions
        - gathers input
        - calls functional core
        - converts decisions into effects
        - should be as dump as possible (domain wise) (so it also takes minimum amount of test cases to verify its behaviour)
#### Comparing Functional & Hexagonal Architecture
- in functional programming everything is immutable & state modification is impossible & side effects are completely pushed to edge of domain operations
- but in hexagonal architecture, domain layer is able to modify states within the same layer
- functional programming can be considered as subset of hexagonal architecture or its radical successor
### Understanding The Drawbacks Of Functional Architecture
#### Applicability Of Functional Architecture
- immutable internal states can be considered as constant values in mathematical functions, not hidden inputs
- collaborators differ from values & are considered as hidden inputs, because
    - they allow modification of their state
    - their behaviour changes by their state
    - this clearly introduces references to internal or external states
## Refactoring Toward Valuable Unit Tests
### Identifying The Code To Refactor
- it usually isn't possible to improve test suite without refactoring underlying production code
#### The Four Types Of Code
- code can be categorized into two dimensions
    1. complexity or domain significance
        - corresponds directly to number of decision making points (branches)
        - calculated using formula of cyclomatic complexity: `1 + <number of branching points using simplest predicates>`
    2. number of collaborators
        - large number of collaborators makes systems hard to test due to maintainability attribute & large arrange phases
- combination of these factors produces four types of code
    1. domain model algorithms
        - few collaborators but high domain complexity
        - most valuable test cases becuase of low maintenance cost, fast feedback & high protection against regressions
    2. trivial
        - few collaborators & zero complexity
        - low value test cases becuase of high maintenance cost & exercising code which has already been tested
    3. controller
        - large number of (usually domain related) collaborators but zero complexity
        - low value test cases becuase of high maintenance cost & exercising code which has already been tested
    4. overcomplicated
        - large number of collaborators & high domain complexity
        - hard to test but too risky to be left without being tested
        - shall be splitted into domain model algorithms & controllers
- the more complexy or significant code is, the less collaborators it should have
#### Using The Humble Object Pattern To Split Overcomplicated Code
- to split overcomplicated code
    - testable parts of it (domain algorithms) are extracted out & called from within it to be used with collaborators
    - remaining code becomes humble object which wraps together domain logic & collaborators
    - this humble object doesn't contain any domain algorithms to be tested & can be treated like controllers
- similarities of functional & hexagonal architectural to humble object pattern
    - domain algorithms
        - immutable core in functional architecture
        - domain layer in hexagonal architecture
    - humble objects themselves
        - application service layer in hexagonal architecture
        - mutable shell in functional architecture
- how humble object pattern enforces single responsibility principle
    - orchestration of collaborators is one responsibility
    - making domain related decisions is one responsibility
    - one piece of code shall take both responsibilities
### Analysis Of Optimal Unit Test Coverage
#### Should You Test Preconditions?
- preconditions which state domain related invariants shall verified by test cases
### Handling Conditional Logic In Controllers
- seperation between domain algorithms & orchestration works best when operations have three distinct stages
    1. retrieving data
    2. executing domain algorithms
    3. presisting data
- but operations may conditionally need to retrieve or store data
- three options are available in such situations
    1. pushing all I/O calls to orchestrators: controllers will retrieve & store all potentially relevant data regardless (reduces performance)
    2. injection of collaborators into domain algorithms: algorithms will directly call collaborators if needed (reduces testability of domain algorithms)
    3. making decision making processes more granular: controllers will act upon each step of operation
        - reduces simplicity of controllers
        - leaks internal state
        - could lead to invariant violations
- three attributes must be balanced in such situations
    1. testability of domain algorithms: derived from number & type of its collaborators, ideally zero
    2. simplicity of controllers: dependes on amount of its involvement in domain decision making process, also ideally zero
    3. performance: relates to number of calls to out of process dependencies & amount of data travelled, ideally as minimum as possible
#### Using The CanExecute/Execute Pattern
- in addition to operations, another function is implemented usually with the name `can_<operation-name>`
- this function shall indicate wether additional data needs to be retrieved, operation must be stopped or etc... by being called within controller
- this function is also called as precondition inside operation itself
- introducing this function will keep protecting application from invariant violations while also letting controllers know if I/O calls should be made
- branches inside controllers which act upon this function aren't considered as part of domain algorithm because they are merely acting on decisions
#### Using Domain Events To Track Changes In The Domain Model
- domain events describe meaningful events for domain experts
- domain events are usually implemented as immutable classes containing data needed to notify external systems about & with names in past tense
- calling specific collaborators as part of observable behaviour is considered as part of domain algorithm
- decision to make such calls shall not be made by controllers
- domain events are used to prevent domain algorithm fragmentation with methods that check if these collaborators should be called
### Conclusion
- keep side effects in memory until operations are finished
- this will make it easy to write test cases for operations with low maintenance cost & without involving out of process dependencies
- its easier to test abstractions than things they abstract (branches & algorithms aren't part of abstractions though!)
- give up hope of separating orchestration from decision making one hundred percent
## Why Integration Testing?
### What Is An Integration Test?
#### The Role Of Integration Tests
- integration tests are tests that fall out of [definitions of unit tests](#the-definition-of-unit-test) which usually verify
    - how the application works with its collaborators (controller code)
    - code that isn't complex but is focused on communications between components (wide code)
#### The Test Pyramid Revisited
- two factors which increase maintenance cost of integration tests
    1. keeping out of process dependencies operationl in order to execute test cases
    2. 3A phases of test cases grow in size with number of collaborators
- two attributes of good test cases provided by integration tests
    1. protection against regression: by exercising more code from both the application & its libraries
    2. resistance to refactoring: by being detached from production code & approching it from POV of its end user
- ration between unit & integration tests
    - as many as possible number of domain edge cases shall be covered by unit tests
    - integration tests shall cover successfull scenarios & edge cases which aren't possible to be tested by unit tests
#### Integration Testing vs. Failing Fast
- fail fast principle
    - can be an alternative to integration test cases
    - stands for stopping current operation as soon as unexpected errors occur (such as preconditions not being met)
    - makes the application more stable by shortening the feedback loop & protecting persistence state
- edge cases leading to application crashes by conforming to fail fast principle shall not be tested
- all communications with all collaborators shall be verified by testing longest successfull scenarios
### Which Out Of Process Dependencies To Test Directly
#### The Two Types Of Out Of Process Dependencies
1. managed
    - fully controlled & only accessible by the application
    - their state isn't directly visible to & doesn't directly affect other applications
    - communications with them are considered as implementation details
    - real instances of them shall be used & their state shall be verified directly when being tested
2. unmanaged
    - not fully controlled by the application
    - accessed directly by other applications
    - communications with them are considered as observable behaviour
    - mocked versions of them shall be used for testing
### Uinsg Interfaces To Abstract Dependencies
#### Interfaces & Loose Coupling
- genuine abstractions are discovered, not invented
#### Why Use Interfaces For Out Of Process Dependencies?
- to enable mocking
- interfaces shall only be introduced for unmanaged out of process dependencies which should be mocked out (which usually exist inside SDKs)
### Integration Testing Best Practices
#### Making Domain Model Boundaries Explicit
- domain model should be within some explicit boundary
- this will help differentiation between controllers & domain algorithms
- making it easy to think about & write unit & integration tests
#### Reducing The Number Of Layers
- extra layers make implementation of features be scattered & puts assumptions on different layers
- also, boundaries between domain algorithms & controllers will be obscured, which will cause overcomplicated code & invaluable test cases
#### Eliminating Circular Dependencies
- circular dependencies happen when two or more classes depend on each other directly or indirectly
- this makes flow execution be scattered across components & obscures entrypoint of flows themselves
- introduction of interfaces to resolve circular dependencies moves this problem from compile time to runtime
- this will not solve problems with circular dependencies
#### Using Multiple Act Sections In A Test
- this is allowed if arrange phase is hard on specific out of process dependencies (or hits certain external limits put by dependencies)
#### Should You Test Logging?
- there are two types of logs
    1. support logging: meant to be used by domain experts
    2. diagnostic logging: meant to be used by developers
- this question can be answered by answering this question: is logging part of observable behaviour of the application?
#### How Should You Test Logging
- standard logging capabilities shouldn't be used for support logging
- support logging is itself considered as domain requirement & should be implemented according
- introducing interfaces can be useful in order to mock & examin communications between the application & logging dependency
## Mocking Best Practices
### Maximizing Mocks' Value
#### Verifying Interactions At The System Edges
- mocking intermediate classes between controller code & unmanaged out of process dependencies violates protection against refactoring attribute because
    - they are related to domain algorithm & may contain code which interprets domain components into terminology of dependencies
    - this code be changed or refactored
    - communications with them are implementation details rather than part of observable behaviours
- only nearest interfaces to out of process dependencies (which directly call or use SDKs) shall be mocked out
- doing this will
    - only verify actual & concrete observable behaviour
    - remove domain related interfaces with one implementation
    - protect backward compatibality
#### Replacing Mocks With Spies
- writing spies only makes sense for adapters of interfaces of unmanaged out of process dependencies which should be mocked out
### Mocking Best Practices
#### Verifying Number Of Calls
- both content & frequency of calls to unmanaged out of process dependencies are considered as observable behaviour
- meaning that existence, absence & content of calls should be verified by test cases
#### Only Mock Types That You Own
- third party libraries should be abstracted by internal adapters because
    - their complexity should be hidden
    - their extra features should not leak into the application
    - this will also protect the application from shotgun surgery when their interface changes
