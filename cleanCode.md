# Clean Code

## Meaningful names

- intentional naming
- noise words & number series
- clarity is the king
- classes & objects
- functions & methods
- one word per one abstraction concept
- solution domain names
- problem domain names
- meaningful context

## Functions

- keep it small
- blocks & indents
- do one thing
  - one thing in it's own abstraction level
  - extract more functions
- one level of abstraction per function
- the stepdown rule
- descriptive names
- arguments
  - monadic
    - operation
    - question
    - event
    - flagged arguments
  - dyadic
    - remove the identical argument
- a function which needs a lot of arguments
- argument lists
- side effects
- command query seperation
- try catch blocks & error handling
- rules to follow when writing big functions

## Comments

- proper use of comments
- my thoughts on comments

## Formatting

- depndent functions
- vertical ordering

## Objects and Data Structures

- the difference
- procedural code
- object oriented code
- choosing between them
- the law of demeter
  - friends
    - class
    - created object
    - passed object
    - the object which is stored in an instance variable of class
  - strangers
- bean methods
- hybrids
- hiding structures
- essential data structures
  - data transfer objects
  - active records

## Error Handling

- try-catch-finally statement
- error handling and logic
- tests which force exceptions
- informative error messages
- exception organizing
- null

## Boundaries

- the natural tension
- third party interfaces
- adapters
- learning tests

## Unit Tests

- laws of tdd
- the tdd cycle
- importance of test code
- clean tests
- build-operation-check pattern
- domain specific language
- one assert per test
- one concept per test
- first rules

## Classes

- encapsulation
- keep it small
- responsibilities
- single responsibility principle
- cohesion
- abstract classes
- concrete classes
- open closed principle
- dependency inversion principle
- interface
- interface segration principle
- what to depend upon

## Systems

- seperation of construct from use
- seperation of main
- factories
- construct method
- dependency injection
- seperation of concerns principle
- control flow
- inversion of control
- contract
- cross cutting concern
- aspect
- aspect oriented programming
- pointcut

## Emergence

- a simple desgin
  - tests
  - duplications
  - expressive
  - minimizing the number of classes and methods
