# unit testing principles, practices & patterns

## the goal of unit testing

the goal of unit testing is to maintain a reasonable balance between debugging, which supports sustainability, & adding or modifying features, which supports scalability. test coverage metrics should not be trusted as measurements because they cannot indicate success against these goals. a successful test suite

- is integrated into the development cycle & ready to run after each commit, pull request, or similar event with minimal effort
- provides maximum value with minimal maintenance cost by verifying only the most important parts of the application, usually domain-related procedures, with effort proportional to the quality of the application code

non-critical code that handles infrastructure, third-party libraries, or dependency provision should be verified briefly or indirectly.

## what is a unit test

most definitions of unit tests emphasize three attributes

1. verification of small pieces of code called units
2. automatic & fast execution
3. isolation & atomicity

there are two schools of unit testing that define isolation differently

1. the london school advocates isolating application components from their collaborators with [test doubles](https://martinfowler.com/bliki/TestDouble.html). this reduces external influence on the SUT, separates behavior from external state, splits the object graph, & reduces preparation code
2. the detroit school advocates isolating test cases & their side effects. it defines units as behaviors that may engage multiple components & categorizes dependencies into four kinds
   1. out-of-process dependencies reside outside the application process & require I/O
   2. shared dependencies allow components to affect each other’s outcomes, usually through mutable state
   3. private dependencies are not shared between components & usually exist in memory
   4. volatile dependencies require runtime-environment setup, such as databases & third-party APIs, & may behave nondeterministically

shared or mutable dependencies are collaborators. immutable dependencies identified only by their content & interchangeable with instances containing the same content are value objects, or values.

| school | advocates isolation of | defines units as | uses test doubles for |
| - | - | - | - |
| london | components | components | mutable dependencies whose state affects behavior |
| detroit | test cases | behaviors | shared dependencies whose state is shared by components |

it is difficult to tell what a test case verifies when it exercises less than a unit of behavior because

> test cases should tell stories about the domain while remaining cohesive & meaningful to domain experts

## the anatomy of a unit test

the 3A pattern structures unit tests into three phases

1. arrange, or given, brings the SUT to the desired state
2. act, or when, invokes the SUT with prepared dependencies & values, then captures its output
3. assert, or then, verifies the result of the act phase, including values, states, or communications

multiple 3A sections may indicate verification of multiple units, which violates the definition of a unit test. avoid `if` statements in test cases because they increase complexity & maintenance cost, reduce readability, & may indicate either verification of too many things or nondeterministic SUT behavior.

arrange phases may be as large as necessary, but [object mother](https://martinfowler.com/bliki/ObjectMother.html) & test data builder patterns can shorten them. act phases should invoke the SUT through a single call. multiple calls in an act phase may indicate a lack of encapsulation, which permits invariant violations.

> invariants are conditions that must remain true at all times

<!-- -->
> protecting code from potential inconsistencies, or invariant violations, is called encapsulation

test cases with identical 3A phases but different values can be grouped through fixtures & parameterized test cases. fixtures are objects in fixed, known states passed as regular arguments before parameterized test cases run. they can serve as SUT dependencies or expected outputs.

parameterized test cases run once for each fixture set & can verify different SUT scenarios & branches. overuse may reduce readability.

modifying one test case should not affect another. shared arrange phases, such as constructors, violate this principle by coupling test cases through hidden assumptions & separating assumptions from the test cases that use them. use factory methods instead to shorten arrange phases while preserving flexibility & readability.

## the four pillars of a good unit test

valuable test cases have four attributes

1. protection against regressions, a test should fail if the SUT stops behaving as expected after refactoring, modification, or development. passing in this situation is a false positive. evaluate this attribute through the volume, complexity, & domain significance of exercised code
2. resistance to refactoring, a test should not fail if the SUT is refactored while preserving behavior. achieve this by decoupling tests from implementation details. failing in this situation is a false negative
3. fast feedback, a test should run quickly & identify its failure cause as directly as possible
4. maintainability, a test should be easy to read, understand, modify, & run

| test result | functional validity | inference | solution |
| - | - | - | - |
| pass | incorrect | false positive | protection against regressions |
| fail | correct | false negative | resistance to refactoring |

protection against regressions, fast feedback, & resistance to refactoring are mutually exclusive, so a test can emphasize only two. because resistance to refactoring is either present or absent, the practical trade-off is between protection against regressions & fast feedback.

the test pyramid recommends a ratio of unit, integration, & e2e tests

- e2e tests at the top favor protection against regressions & black-box testing based on external specifications
- integration tests in the middle balance both
- unit tests at the bottom favor fast feedback & white-box testing based on internal components

## mocks & test fragility

test doubles are fake dependencies passed to the SUT instead of real ones to reduce arrange-phase maintenance costs. they have two main variations

1. mocks emulate & examine outgoing interactions
   - regular mocks are created with mocking libraries
   - spies are handwritten mock objects
2. stubs emulate incoming interactions
   - regular stubs are smart objects with configurable behavior
   - dummies only satisfy method signatures & may return hard-coded fake values
   - fakes are like regular stubs but substitute components that do not yet exist

observable behavior is the opposite of implementation detail. it exposes operations or states to satisfy clients directly. an operation is a method that calculates, produces side effects, or both.

a component’s public API should be limited to observable behavior, & every client need should be fulfilled through a single operation. otherwise, APIs leak implementation details, weaken encapsulation, & permit invariant violations.

communications with stubs are not observable behavior because they occur through incoming interactions. verifying stub interactions couples tests to SUT implementation details & violates resistance to refactoring. methods on the same object may still be treated separately as mocks or stubs.

under the CQS principle, a method should be either a command that produces side effects without returning a value or a query that returns a value without side effects. mocks substitute commands & stubs substitute queries.

hexagonal architecture emphasizes three guidelines

1. separate domain & technical concerns through layers
   - the domain layer is isolated, stateless, & contains domain algorithms
   - the application service layer coordinates collaboration & orchestration without making domain decisions
2. limit internal communication by preventing domain-layer components from depending on application-service-layer components
3. structure communication between applications through common interfaces in their application service layers

each layer has its own observable behavior & implementation details. because the application service layer is a client of the domain layer, test cases that cover components across layers may overlap.

communication inside applications is intra-system communication. it occurs between application components & is not directly visible or relevant to clients. communication between applications is inter-system communication. it is an outcome or side effect & therefore observable behavior.

emulate intra-system communication with stubs. emulate inter-system communication with mocks. inter-system communication occurs through interfaces, is sensitive to refactoring, & should be examined & protected by test cases.

parallel test execution requires isolation of side effects, including shared dependencies. non-out-of-process dependencies can be instantiated per test case. creating a separate process for every out-of-process dependency is usually impractical, so such dependencies can be replaced with test doubles.

if a shared out-of-process dependency is accessible & visible only to one application, treat it as part of that application. communication with it is not observable behavior, is not sensitive to refactoring, & is not inter-system communication. mocking it violates resistance to refactoring.

## styles of unit testing

there are three unit-testing styles

1. output-based, also called functional, verifies SUT outputs for specific inputs. it is the best style when applicable & requires functional code without side effects or dependencies
2. state-based, preferred by the detroit school, verifies the state of the SUT or its dependencies. extreme use may violate resistance to refactoring by coupling tests to the SUT API or harm maintainability through large, complex assert phases
3. communication-based, preferred by the london school, uses test doubles to verify communication between the SUT & collaborators. extreme use may weaken protection against regressions by exercising too little behavior, violate resistance to refactoring through internal communication checks, or harm maintainability with complex arrange & assert phases, including mock chains

to use output-based tests, write the SUT as pure functions. pure functions have no hidden inputs or outputs, such as side effects, exceptions, or references to mutable internal or external state like time, dates, data stores, or collaborators. their inputs & outputs are explicit in their signatures. immutable internal state can be treated as constants.

pure functions produce the same output for the same input regardless of time, state, or context, making them deterministic. they can be replaced by the values they return, which is referential transparency.

functional architecture is a radical successor to hexagonal architecture. it pushes side effects to the edge of domain operations, maximizes pure functional code, & minimizes non-functional code through these boundaries

- the functional core, also called the mutable core, contains domain algorithms, makes decisions, uses pure functions, & does not depend on the mutable shell
- the mutable shell gathers input, depends on the functional core, & turns its decisions into side effects. it should be as simple as possible & make no domain decisions

## refactoring toward valuable unit tests

code can be measured across two dimensions

1. complexity or domain significance, corresponding directly to the number of decision points or branches
2. number of collaborators

combining these dimensions produces four code types

1. domain model algorithms have few or no collaborators & high domain complexity. their tests are highly valuable because of low maintenance cost, fast feedback, & strong protection against regressions. they should also verify domain preconditions
2. trivial code has little or no complexity & few or no collaborators. tests for it are usually not valuable
3. controller code has little or no complexity but many collaborators. test it with the communication-based style to examine orchestration because most output is already verified by tests of domain algorithms
4. overcomplicated code has high domain complexity & many collaborators. its tests have high maintenance cost, weak resistance to refactoring, & weak protection against regressions. split it into domain algorithms & controllers

the humble object pattern simplifies overcomplicated code by extracting complex, testable domain algorithms into separate procedures. the remaining humble object connects domain algorithms with collaborators, similar to a controller.

orchestrating collaborators, or being wide, & making domain decisions, or being deep, are separate responsibilities. a component should do one or the other, but not both.

separating domain algorithms from controllers works best when operations follow three stages

1. retrieving
2. calculation or decision-making
3. persisting

in practice, operations may conditionally retrieve or persist data. three options exist

1. move all potentially required I/O to controllers, which can reduce performance through unnecessary I/O
2. inject collaborators into domain algorithms, which reduces the quality of their tests
3. split operations into granular steps so controllers perform I/O when necessary, which complicates controllers, weakens their tests, leaks internal state, weakens encapsulation, & permits invariant violations

balance these attributes

1. testability of domain algorithms, determined by the number & type of collaborators, ideally zero
2. simplicity of controllers, determined by their involvement in domain decision-making, ideally none
3. performance, determined by the number of I/O calls & the data sent & received through them, ideally minimal

the can/execute pattern is another option. alongside operations, implement procedures usually named `[can | should]_...` that accept already retrieved data & indicate whether further I/O is needed, the operation must stop, or another action is required. controllers call these procedures to perform only necessary I/O, & domain algorithms use them as preconditions.

this preserves encapsulation while allowing controllers to determine whether I/O should occur. controller branches that act on these procedures are not domain complexity because they act on decisions rather than make them.

describe meaningful events for domain experts as domain events. they are typically immutable components containing the data required to notify external systems & are named with past-tense verbs. domain events can prevent domain algorithms from fragmenting into methods that merely tell controllers whether collaborators should be called.

## why integration testing

integration tests are test cases that do not meet the definition of unit tests. they typically verify communication between the application & its collaborators, usually through controller code rather than domain complexity.

keeping out-of-process dependencies operational & using large 3A sections increases integration-test maintenance cost. however, integration tests offer stronger protection against regressions by exercising more code & layers, plus stronger resistance to refactoring by verifying complete operations rather than atomic units. cover successful scenarios, edge cases not covered by unit tests, & domain edge cases.

an alternative is the fail-fast principle, which stops an operation as soon as an unexpected error occurs or a precondition is violated. it improves stability by shortening the feedback loop & protecting persistence state. integration tests can ignore edge cases that cause application crashes due to this principle.

there are two types of out-of-process dependencies

1. managed dependencies are fully controlled & only accessible by the application. their state is not directly visible to or affected by other applications. communication with them is an implementation detail, so they should not be mocked & their state should be verified directly
2. unmanaged dependencies are not fully controlled by the application & may be accessed directly by other applications. communication with them is observable behavior & should be verified with mocks

> genuine abstractions are discovered, not invented

internal interfaces for unmanaged out-of-process dependencies enable mocking in tests. mock dependencies through known, owned interfaces rather than provider interfaces, which often belong to SDKs. internal interfaces hide service complexity & protect against shotgun surgery when external interfaces change.

define an explicit, shared boundary around domain algorithms before writing tests. this makes unit & integration tests easier to reason about & write.

extra layers scatter feature implementation, distribute assumptions across locations, make features harder to test, & obscure boundaries between domain algorithms & controllers. this produces overcomplicated & trivial code, which leads to low-value tests.

circular dependencies scatter execution flows across components & increase test maintenance costs. adding interfaces to resolve circular dependencies does not solve the underlying problem, but moves it from compile time to runtime.

multiple act phases in one test case are allowed only when the arrange phase is too difficult or expensive.

logging is either technical diagnosis for developers or a domain requirement for domain experts. the latter is support logging, which is observable behavior & should not use standard logging facilities. support logging involves I/O, & its destination can be treated as an unmanaged out-of-process dependency. introduce interfaces so the requirement can be implemented appropriately & logs can be verified with mocks.

## mocking best practices

when verifying communication, do not mock intermediate classes. doing so violates protection against refactoring because these classes are application code that may contain, engage with, or represent domain components that can change during refactoring.

mock only the final interface in the call stack that causes the actual external communication because that is where observable behavior occurs. when a dependency is hidden behind an interface dedicated solely to that dependency, mock the adapter.

this verifies concrete observable behavior, allows removal of domain interfaces with only one implementation, preserves backward compatibility, & maintains resistance to refactoring without weakening protection against regressions.

both the content & number of calls to unmanaged out-of-process dependencies are observable behavior & should be verified by test cases.

## testing the database

store database schemas & upgrade scripts, called migrations, in version control. this creates a single source of truth for schema state, makes changes traceable, & allows ready-to-use database instances to be created on demand. do not modify migrations after committing them unless applying them would cause data loss. treat reference data as part of the schema & keep it with migrations.

> reference data is prepopulated data required for the application to operate properly & is usually never modified by the application

execute data modifications from one operation atomically by separating two responsibilities

1. repositories determine which data should change & use or expect transactions
2. transactions determine whether those changes are committed

controllers then orchestrate transactions, repositories, & domain algorithms as separate collaborators. controllers call transaction `commit` & `abort` methods because doing so requires a decision, including implicit decisions on happy paths.

the unit of work pattern applies this separation of concerns. it wraps the transaction object, tracks data modifications, & avoids unnecessary database calls until committing becomes necessary. a regular transaction object instead manages data state within a database-managed scope outside the application process.

whether using transaction objects or the unit of work pattern, every test phase must use its own physical transaction rather than sharing one.

a managed out-of-process dependency shared across test cases prevents parallel execution. although solutions exist, this limitation is usually better accepted. shared database state also requires cleanup that removes leftover test data & restores an initial state. perform cleanup in the arrange phase or teardown methods, but do not remove reference data.

## extra

- http://mng.bz/KE9O
- https://martinfowler.com/bliki/TellDontAsk.html
- https://enterprisecraftsmanship.com/posts/ocp-vs-yagni
