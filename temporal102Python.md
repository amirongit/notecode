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
### Logging In Workflows & Activities
- using loggers from temporal SDK enables suppressing logs during state restoration (event history replay) possible
- `temporalio.workflow.loggier` is used to log in workflows
- `temporalio.activity.loggier` is used to log in activities
### Accessing Workflow Results
- `temporalio.workflow.execute_workflow` requests workflow execution & awaits execution result
- `temporalio.workflow.execute_workflow`
    - requests workflow execution
    - returns instance of `temporalio.client.WorkflowHandle`
    - `result` method on returned object is awaited to obtain workflow execution result
### Accessing Activity Results
- `temporalio.workflow.{execute_activity,execute_activity_method,execute_activity_class}` request activity execution & await execution result
- `temporalio.workflow.{start_activity,start_activity_method,start_activity_class}`
    - request activity execution
    - return instance of `asyncio.Task`
    - returned object is awaited to obtain activity execution result
## Using Timers In A Workflow Definition
### What Is A Timer?
- temporal provides durable timers
- durable timers are used to introduce delays into workflow executions
- durable timers are maintained by temporal cluster
- associated workers won't use any resource while execution of workflows are blocked by durable timers & will continue polling tasks
- durable timers with less than one second of blocking are encouraged to be avoided
- usually used to enable dynamic amount of blocking
### Timer APIs Provided By The Python SDK
- python SDK implements [custom event loop](https://temporal.io/blog/durable-distributed-asyncio-event-loop)
- all async related operations from `asyncio` library can be used in context of temporal (sleep, create tasks, execute activities with timeout, etc...)
## Understanding Event History
### Workflow Execution Overview
- workflow executions are identified by "run id"
- workflow executions could be in one of two states
    1. open (currently running; cycling between progression & awaiting execution results)
        1. [continued as new](https://docs.temporal.io/develop/python/continue-as-new)
    2. closed
        1. completed
        2. failed
        3. canceled
        4. terminated
        5. timed out
- closed workflow executions can't be opened again
### Overview Of Event History
- temporal cluster maintains an ordered append only log of immutable events per each workflow execution
    - used to reconstruct state of executions
    - enables developers to debug specific executions
    - persisted in temporal database
- event histories always start with "WorkflowExecutionStarted"
### Event History Limits
- both number of events & size of event histories are limited by temporal cluster
- number of events is limited to around 50k events
- `temporalio.workflow.info().is_continue_as_new_suggested` & `workflow.continue_as_new` are used to avoid reaching event history count limits
- size of input parameters, returned values & variables are limited to 2MB in total
- size of event history is limited to 50MB
- [claim check pattern](https://www.enterpriseintegrationpatterns.com/patterns/messaging/StoreInLibrary.html) is used to avoid reaching event history size limits
## Understanding Workflow Determinism
### History Replay: How Temporal Provides Durable Execution
- commands & event histories of workflows are replayed in order
- history replay avoids duplicated execution of activity or workflows (execution results are accessible through event history)
### Why Temporal Requires Determinism For Workflows
- determinism enables temporal to achive exact state of previous executions through history replay
- activities have the ability to inject non deterministic values into the event history
### Python Sandbox Environment
- temporal python SDK executes workflow code inside sandbox
- the sandbox will raise exceptions if non deterministic events happen
- passed through mechanism of sandbox is used to import non deterministic modules (which calls to should be deterministic)
- most parts of standard library of python & temporal python SDK itself are passed through by default
- the sandbox is consisted of two parts
    1. global state isolation (uses `exec` to compile & evaluate statements)
    2. restrictions (prevents known non deterministic library calls like `random.*`, `datetime.datetime.now`, etc...)
### Common Sources Of Non Determinism
- external systems or states
- unordered iteration
- random values
- system time
- threads
- run id
### How Workflow Changes Can Lead To Non Deterministic Errors
- deploying modifications of workflows in ways that break input, path, & output of workflows while there are open executions of them
- these would cause errors
    - adding, removing & switching activity calls
    - adding or removing timers
    - altering execution order
- these wouldn't
    - modifying statements which do not affect generated commands
    - changing `ActivityOptions` or `RetryPolicy`
    - modifying activity code
    - changing duration of timers (?)
## Testing Your Temporal Application Code
### Testing Activities
- `temporalio.testing.ActivityEnvironment.run` can be used to execute activities in test code (without engaging cluster)
### Testing Workflows
- static methods of `temporalio.testing.WorkflowEnvironment` can be used to create test environment of running temporal server instance
- instance of `temporalio.worker.Worker` can be created using the test client in order to execute workflows
