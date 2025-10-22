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
## How Errors Affect Workflow Execution
### Activity Errors
- custom & pre defined retry policies can be specified upon calling activities
- default retry policy is to retry activities in exponential back off manner upon failure (this ensures handling temporary problems)
- activities are encouraged to be [idempotent](https://en.wikipedia.org/wiki/Idempotence) since they could be tried multiple times
- it is possible to not retry at all upon certain exceptions being raised
### Workflow Errors
- workflow task failures
    - exceptions that don't extend `temporalio.exceptions.FailureError`
    - represent an unexpected situation in workflow process
    - will cause workflow execution to be retried (if there are associated retry policies)
- workflow execution failures
    - exceptions that usually extend `temporalio.exceptions.ApplicationError` (subclass of `temporalio.exceptions.FailureError`)
    - will put workflow execution to "failed" state
    - will cause workflow execution to not be retried
- there isn't any retry policies associated to workflow calls by default
## Improving Your Temporal Application Code
- workflows & activities are able to accept any number of parameters in most serializable formats
- changing orders & formats of input or output parameters can negate backward compatibility
- it is encouraged to use dataclasses or protobufs for inputs & outputs
    - enhance & allow backward compatibility
    - allow adding or changing types of arguments without breaking backward compatibility
    - don't break ongoing executions upon changing
