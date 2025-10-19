# Understanding Key Concepts In Temporal
## Durable Execution System
### What Is A Durable Execution System
- guarantees successfull, relatable & correct execution of application code
- maintains state in order to allow applications recover from unexpected conditions
### Developer Productivity
- high level abstractions provided by temporal enable
    - low effort scalability
    - development without considering unexpected situations
## Temporal Application Structure
- workflows
    - core abstraction of temporal
    - represent sequence of steps used to carry out business logic
    - implemented in different programming languages using SDKs provided by temporal itself
    - required to be determenistic
- activities
    - encapsulate unreliable or non deterministic code
    - retried upon failure
- workers
    - responsible for code execution
    - poll task queues maintained by temporal cluster
    - implemented by temporal SDK & configured in code
- cluster
    - orchestrates execution
    - manages workers
<!-- ## How Errors Affect Workflow Execution -->

