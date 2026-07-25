# Unit Testing: Principles, Practices & Patterns
## The Goal Of Unit Testing
the goal of unit testing is to keep a reasonable ratio between debugging (sustainability) & adding or modifying features (scalability). test coverage metrics shouldn't be tusted as measurements because they can't indicate positiveness with these definitions of goals. a successfull test suite is one that is:
- integrated into the development cycle, meaninig that it is ready to be executed after each commit or pull request or such events with minimum effort
- provides maximum value with minimum maintenance cost, meaning that it verifies only the most important parts of the application
  (usually procedures related to the domain) & does it with low effort, which obviously depends on the quality of the code of the application

non critical code (which handles infrastructure & third party libraries or deals with providing dependencies) should be verified briefly or indirectly.
## What Is A Unit Test?
essential attributes among most definitions of unit tests emphasize on three attributes:
1. verification of small pieces of code (called units)
2. automatic & quick execution
3. isolated & atomic

there are two schools of unit testing which define the isolation attribute differently:
1. the london school advocates for isolation of the components of the application from their collaborators by using [test double](https://martinfowler.com/bliki/TestDouble.html)s, which will reduce the amount of external influence on the SUT (system under test) causing separation of its behaviour from external state & split object graph causing reduction of the amount of preparation code
2. the detroit school advocates for isolation of test cases & their side effects & defines units as behaviours in which multiple components may be engaged; it also categorizes dependencies into four kinds & handles each of them differently:
    1. out of process dependencies, residing outside of the application's execution process & calling them involves I/O
    2. shared dependencies, which provide ways for components to affect each other's outcome (usually a mutable field)
    3. private dependencies, which aren't shared between components & are usually in memory
    4. volatile dependencies, which require runtime environment setup (like databases & 3rd party APIs) & may behave non deterministically

shared or mutable dependencies are called collaborators. immutable dependencies which are identified only by their content & are interchangeable with other instances having the same content are called value objects (or values).

|school|advocates for isolation of|defines units as|uses test doubles for|
|-|-|-|-|
|london|components|components|mutable dependencies (their state affect their behaviour)|
|detroit|test cases|behaviours|shared dependencies (their state is shared by components)|

it is hard to tell what exactly a test case verifies if it exercises something less than a unit of behaviour, because:
> test cases should tell stories about domain, being cohesive & meaningful to domain experts

## The Anatomy Of A Unit Test
the 3A pattern can be used to define a structure of unit tests, using this pattern, test cases are splitted into three phases:
1. arrange (given), in which the SUT is brought to the desired state
2. act (when), in which the SUT is invoked with dependencies & values prepared in arrange phase & its output is captured
3. assert (then), in which the end result of the invokation in act phase is verified, which might include values, states & communications

multiple 3A sections might indicate verification of multiple units, which violates the definition of unit tests. if statements also should be avoided in test cases because they increases complexity & maintenance cost, reduce readability & might indicate either verification of too many things at once or non deterministic behaviour of the SUT.

arrange phases can be as large as they have to be, but [object mother](https://martinfowler.com/bliki/ObjectMother.html) & test data builder patterns could be used to shorten them. act phases on the other hand, should be limited to invoking the SUTs by a single call; doing more than that in an act phase indicates lack of encapsulation, which allows invariant violations.
> invariants are conditions which shall hold true at all times

<!-- -->
> the act of protecting code against potential inconsistencies (invariant violations) is called encapsulation

test cases having the same 3A phases but with different values can be grouped together & be written as one by using fixtures & parameterized test cases; fixtures are objects in fixed & known states passed as regular arguments to parameterized test cases before their execution & can be used as dependencies of the SUTs or their expected outputs.

parameterized test cases are executed once per set of fixtures & can be used to verify different scenarios & branches of the SUT; overusing them may reduce readability.

modification of test cases should not affect each other. having a shared arrangement phase (for example, in constructors) will violate this principle. this will couple test cases together by allowing common & hidden assumptions between them & causes them to be less readable by separating their assumptions from themselves. factory methods can be used instead of hidden shared arrangement phases in order to shorten arrangement phases without the mentioned drawbacks & with more flexibality & readability.
## The Four Pillars Of A Good Unit Test
valuable test cases have four attributes:
1. protection against regression: if the SUT stopped behaving as expected due to refactoring, modification or development (this is called regression), the test case should fail; not failing in this situation is called a false positive; this attribute is evaluated by the amount of volume & complexity of exercised code & its domain significance
2. resistance to refactoring: if the SUT is refactored & still behaves as expected, the test case should not fail; this attribute is achieved by decoupling test cases from implementation details of the SUTs; failing in this situation is called false negative
3. fast feedback: the test case should run quickly & point to its failure cause as directly as possible
4. maintainability: the test case should be easy to read, understand, modify & execute

|test result|functional validity|inference|solution|
|-|-|-|-|
|pass|correct|true positive|-|
|pass|incorrect|false positive|protection against regressions|
|fail|incorrect|true negative|-|
|fail|correct|false negative|resistance to refactoring|

protection against regression, fast feedback & resistance to refactoring are mutually exclusive & test cases are capable of only emphasizing two of them. since resistance to refactoring is either conformed or not, the trade off is reduced to the other two attributes. the test pyramid advocates for certain ratio of unit, integration & e2e tests, moving toward each of these two on each layer:
- e2e tests (the top layer): favor protection against regressions & black box testing (based on external specifications)
- integration tests (the middle layer): favor both equally
- unit tests (the bottom layer): favor fast feedback & white box testing (based on internal components)
## Mocks & Test Fragility
test doubles are objects passed as fake dependencies instead of the real ones to the SUT in order to reduce maintainability cost of arrange phases; there are two variations of them having their own sub variations:
1. mocks: used to emulate & examin outgoing interactions
    - regular mocks: mock objects created with mocking libraries
    - spies: hand written mock objects
2. stubs: used to emulate incoming interactions
    - regular stubs: smart objects with configurable behaviour
    - dummies: objects that only satisfy method signatures & may return hard coded & fake values
    - fakes: objects like regular stubs but used as substitutes for not yet existing components

observable behaviour is the opposit of implementation detail; it is code that exposes operations or states in order to satisfy clients directly. an operations is a method that calculates, incurs side effects or both.

public API of components should be limited to their observable behaviour & any individual need of the clients should be achieved through a single operation. otherwise, this indicates leaking of implementation details through APIs (lack of encapsulation) which allows invariant violation.

communications with stubs aren't part of observable behaviour because these behaviours can't happen through incoming interactions. therefore, verifying interactions with stubs in test cases violatest the resistance to refactoring attribute by coupling the test case with implementation details of the SUTs. different methods on the same object can be separatedly considered as mocks or stubs though.

from the POV of the CQS principle, which states taht a method should either be a command (produce side effects without returning values) or a query (return values without producing side effects), mocks substitute commands & stubs substitute queries.

hexagonal architecture emphasizes on three guidelines:
1. separation of domain & technical concerns, by defining these layers
    - domain layer: which is isolated & stateless & contains domain algorithms
    - application service layer: which is focused on collaboration & orchestration, without making domain related decisions but acting upon them
2. limiting communications inside the application, by perventing domain layer components depend on application service layer components
3. structuring communications between the applications by common interfaces within their application service layers

in the context of hexagonal architecture, each layer has its own observable behaviours & implementation details. application service layer is client of the domain layer, therefore, test cases working on components of different layers might have overlaps.

communications inside applications are either intra system, meaning that they happen between components of the application & aren't directly related or visible to clients, or inter system, meaning that they happen between multiple applications & considered as outcome or side effects, thus, part of the observable behaviour.

intra system communications are emulated by stubs but inter system communications should be emulated by mocks. the latter happens through interfaces & is sensetive to refactoring, therefore, should be examined within & protected by test cases.

in order for test cases to run in parallel, their side effects (thus, shared dependencies) should be isolated from each other. non out of process dependencies can be instantiated per test case. but it isn't practical to spawn a new process of out of process dependencies for each test case; therefore, these kind of dependencies are replaceable by test doubles.

if a shared out of process dependency is only accessible by & visible to only one application, it should be considered as part of the application itself. communications between the application & such dependencies aren't part of its observable behaviour, aren't sensetive to refactoring & aren't categorized as inter system communications; therefore, using mocks for such dependencies violates the resistance to refactoring attribute.
## Styles Of Unit Testing
there are three styles of unit testing:
1. output based (aka functional): this is the bets style; it verifies outputs from the SUT for specific inputs; it is only applicable to functional (side effect free & without dependencies) code
2. state based: this style is preferred by the detroit school; it verifies state of the SUT or its dependencies; its extreme cases may violate resistance to refactoring attribute by being coupled too much with the API of the SUT or maintainability attribute by having large & complicated assert phases
3. communication based: this styles is preferred by the london school; it uses test doubles to verify communications between the SUT & its collaborators; its extreme cases may violate protection against regressions attribute by exercising too little amounts of code or behaviour or resistance to refactoring attribute by being highly coupled to implementation details due to verifying internal communications or maintainability attribute by having large & complicated arrange & assert phases which might include mock chains (mocks that return mocks)

in order to apply output based style test cases, the SUT must be written in pure functions. pure functions don't have hidden inputs or outputs suchs as side effects, exceptions & references to mutable internal or external states like date, time or data stores & collaborators. their inputs & outputs are explicitly expressed by their method signatures & if they use immutable internal states in their procedures, they can be considered as constants. they produce the same outputs for the same input regardless of time, states or situations & therefore, are deterministic. they can be replaced by the values they return (this is called referential transparency).

functional architecture is the radical successor of hexagonal architecture which pushes side effects to the edge of the domain operations & maximizes purely functional code & minimizes non functional code by defining these boundaries:
- functional core (aka mutable core): contains domain algorithms, makes decisions, is implemented using pure functions & doesn't depend on the mutable shell
- mutable shell: gathers inputs, depends on the functional core & acts upon its decisions by converting them into side effects. it is as dumb as possible & doesn't make any domain related decisions.
## Refactoring Toward Valuable Unit Tests
it is possible to measure code in two dimensions:
1. complexity or domain significance: which corresponds directly to the number of decision making points (branches)
2. number of collaborators

combination of these dimensions produce four types of code:
1. domain model algorithms: code which deals with zero to few collaborators but contains high amount of domain complexity; test cases verifying this type of code are the most valuable because of low maintenance cost, fast feedback & high protection against regressions & should also verify domain related preconditions
2. trivial: code which contains near to none complexity & deals with zero to few collaborators; test cases verifying this type of code are worthless
3. controller: code which contains near to none complexity but deals with high number of collaborators; test cases verifying this type of code should use the communication based style in order to examin orchestrations, because most of their output will be already verified by test cases which verify the first type
4. overcomplicated: code which contains high amount of domain complexity & deals with high number of collaborators; test cases verifying this type of code have high maintenance cost, low resistance to refactoring & low protection against regressions; but it can't be left out because it contains domain complexity; this type of code should be splitted into domain algorithms & controllers in order to achieve test cases with high value

the humble object pattern can be used to simplify overcomplicated code. using this pattern, complex & testable parts of the component (domain algorithms) are extracted out into separate procedure & replaced by calls. what remains of the component becomes a humble object which glues together domain algorithms & collaborators, which is similar to what a controller does.

orchestration of collaborators (being wide) & making domain related decisions (being deep) are two responsibilities (kinds of being); a single component should do (or be) either but not both.

the separation between domain algorithms & controllers works bets when operations have these three distinct stages in order:
1. retrieving
2. calculation (or decision making)
3. presisting

but in practical cases, operations may conditionally decide to retrieve or presist data. three solutions exist for these situations:
1. pushing & doing all potentially necessary I/O calls to & in controllers, regardless: this will reduce performance because of potentially unnecessary I/O calls
2. injection of collaborators into domain algorithms: this will reduce the quality of test cases of domain algorithms
3. making operations more granular by splitting them into steps which lets controllers do I/O calls if necessary: this will reduce simplicity of controllers & quality of their test cases & leak internal state which weakens encapsulation & allows invariant violations

these three attributes must be balanced in these situations:
1. testability of domain algorithms: derived from the number & type of their collaborators, ideally zero
2. simplicity of controllers: derived form the amount of its involvement in domain decision making process, ideally none
3. performance: derived from the number of I/O calls (specifically, calls to out of process dependencies) & amount of data sent & recieved through these calls, ideally as low as possible

can/execute pattern is another solution for these situations. using this pattern, in addition to operations themselves, other procedures are implemented (usually named as `[can | should]_...`) which expect already retrieved data & indicate if additional I/O calls should be done or the operation must stop or etc; these procedures are then called by controllers in order to do only necessary I/O calls. these procedures should also be used as preconditions in domain algorithms themselves. using this pattern will keep encapsulation while also letting controllers know if I/O calls should be made. branches inside controllers which act upon the output of these procedures aren't considered as domain complexity because they are merely acting on decisions, not making them.

meaningful events for domain experts should be described (or modeled) by domain events; these are usually implemented as immutable components containing necessary data to notify external systems, named using past tense verbs. domain events can be used to prevent fragmentation of domain algorithms with methods indicating to controllers if some collaborators should be called or not.
## Why Integration Testing?
integration tests are test cases which don't fit into the definitions of unit tests. these test cases usually verify communications between the application & its collaborators; components verified by them don't contain domain complexity but are focused on collaboration (controller code).

the requirement to keep the out of process dependencies operationl & big 3A sections increase the maintenance cost of integration tests. on the other hand, integration tests provide better protection against regressions (by exercising more code of more layers) & resistance to refactoring (by verifying whole operations rather than atomic units). these tests should cover all successfull scenarios, edge cases which aren't covered by unit tests & domain edge cases.

an alternative to integration tests is the fail fast principle. it stans for stopping the current operation as soon as an unexpected error occurs or a precondition is violated. it makes the application more stable by shortening the feedback loop & protects the persistence state. edge cases leading to application crashes caused by this principle should be ignored in integration tests.

there are two types of out of Process dependencies:
1. managed: these dependencies are fully controlled & only accessible by the application; their state isn't directly visible to & doesn't directly affect other applications; communications with them are considered as implementation details; they shouldn't be mocked in test cases & their state should be verified directly
2. unmanaged: these dependencies aren't fully controlled by the application; they are accessed directly by other applications; communications with them are considered as observable behaviour & should be verified & examined using mocks

> genuine abstractions are discovered, not invented

having internal interfaces for unmanaged out of process dependencies enables mocking them in test cases. it is better to mock dependencies through known & owned interfaces rather than their provided interfaces (which usually reside in SDKs). internal interfaces hide extra complexities of the services they abstract & protect the application against the possibility of shotgun surgery in case of changes in external interfaces.

domain algorithms should be within some explicit & common boundary before writing test cases. this will make it easy to think about & write unit & integration tests.

extra layers make implementation of features scattered & enforce assumptions on different places; making it hard to test features & obscuring the boundaries between the domain algorithms & controllers, causing overcomplicated & trivial code which themselves cause invaluable test cases.

circular dependencies make flow executions scattered across multiple components which causes maintenance cost of test cases to be increased. introduction of interfaces to resolve these kinds of dependencies doesn't solve the real problem, but moves it from compile time to runtime.

having multiple act phases in a single test case is only allowed if the arrange phase is too hard or too expensive.

logging is done either for technical diagnosis (meant to be used by developers) or to satisfy domain requirements (meant to be used by domain experts). the latter is called support logging, considered as part of observable behaviour & shouldn't be done using standard facilities. support logging involves I/O & the destination can be viewed as an unmanaged out of process dependency; therefore, interfaces should be introduced in order to implement such requirement according to the requirement & enable mocking to verify & examin logs.
## Mocking Best Practices
when verifying communications, intermediate classes shouldn't be mocked. doing so violates the protection against refactoring attribute because these classes are part of the application code & may engage with, contain or be domain related components which may be changed or refactored. only the latest interface in the call stack which causes the actual communication should be mocked because that's where observable behaviour happens. if the dependency is abstracted behind an interface whose only job is to abstract that single dependency, the adapter should be mocked.

doing this will only verify actual & concrete observable behaviour, let domain related interfaces with only one implementation be removed, protect backward compatibality & keep the resistance against regressions attribute while also not violating the protection against refactoring attribute.

both content & number of calls to unmanaged out of process dependencies are considered as observable behaviour & should be verified by test cases.
## Testing The Database
the database schema & its upgrade scripts (called migrations) should be stored within a version control system; doing this will maintain a single source of truth about state of the database schema & makes it easy to track changes & to setup new instances of it with its components ready, on demand. migrations should not be modified once commited to the VCS unless their appliance would lead to data loss. reference data should also be considered as part of the schema & kept along with migrations.
> reference data is data that must be perpopulated in order for the application to operate properly & the application usually won't modify it ever

data modifications caused by a single operation should be executed in an atomic manner which is done by separating two responsibilities from each other:
1. what parts of data should be modified: handled by repository classes using (or expecting) transactions
2. wether the modifications should be commited or not: handled by transactions

controllers will then be orchestrating transactions, repositories & domain algorithms as separate collaborators. commit & abort methods of the transaction object will be called by controllers because calling them requires a decision (implicit decisions in the case of happy paths).

unit of work pattern uses this separation of concerns, wraps the transaction object, keeps track of data modifications & avoids unnecessary database calls by the time that it is decided wether the transaction should be commited or not. in contrast, a usual transaction object will maintain state of data within its scope managed by the database itself (which happens outside of the process of the application). wether transaction objects are used or unit of work pattern, each phase in test cases must use their own physical transaction & not share them with each other.

managed out of process dependency which is shared between test cases removes the possibility of execution of test cases in parallel; there are solutions to this but better be accepted. also, commonality of the database among the test cases forces a step in test cases in which left over data is removed & the database is brought to an initial phase; this can be done in the arrange section or in teardown methods; reference data should not be removed while cleaning left over data from other test cases.
## Extra
- http://mng.bz/KE9O
- https://martinfowler.com/bliki/TellDontAsk.html
- https://enterprisecraftsmanship.com/posts/ocp-vs-yagni
