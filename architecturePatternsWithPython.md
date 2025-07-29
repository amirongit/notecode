# Architecture Patterns With Python
## Building An Architecture To Support Domain Modeling
### Domain Modeling
#### What Is A Domain Model
- term from DDD jargon which replaces "business logic layer"
- mental map that business owners have of their business
- emerges naturally with its own jargon among stake-holders
- domain
    - means the problem being solved
    - automated business processes
- model
    - map of process or phenomenon
    - captures properties
- entities
    - used to model business concepts which have persistent identities
    - their identities aren't changed when their values do so
- value objects
    - used to model business concepts which hold data but no identity
    - identified by their data
    - usually immutable
    - could support mathematical operations
- domain functions
    - justified when an operation doesn't belong to an specific model
- domain exceptions
## Event Driven Architecture
### Dependecny Injection (And Bootstrapping)
