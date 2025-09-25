# Unit Testing: Principles, Practices & Patterns
## The Goald Of Unit Testing
### The Of Unit Testing
- keeping reasonable ratio between coding or debugging time & adding or modifying features (sustainability & scalability)
#### What Makes A Good Or Bad Test?
- test code also has maintenance cost
### Using Coverage Metrics To Measure Test Suite Quality
- coverage is good negative & bad positive indicator tool
#### Understanding The Code Coverage Metric
- ratio between lines executed by test suite & all of code
- easy to manipulate by making code more compact  (using inline syntaxes, etc...)
- aka test coverage (?)
#### Understanding The Branch Coverage Metric
- ratio between exercised by test suite & all branches of code
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
- unit tests shall verify important parts of code (usually the domain model)
- non critical code should be verified briefly or indirectly
    - infrastructure
    - third party
    - wireup
#### It Provides Maximum Value With Minimum Maintenance Costs
- writing valuable unit test isn't possible without properly structured & written code
