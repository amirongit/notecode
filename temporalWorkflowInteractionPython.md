# Interacting With Workflows In Python
## Signaling Your Workflows
### What Are Signals?
- asynchronously sent messages to open workflows
- used to change state or flow of workflows
- useful for workflows that should react to external events
### Developing Signals
- to define signals
    - name & data structure of the signals are specified
    - `temporalio.workflow.signal` is used to define signal methods on workflow definition classes
- to handle signals
    - usually signal methods expose data to outside of their own scope
    - it is encouraged to use `temporalio.workflow.wait_condition` instead of `asyncio.sleep` when awaiting signals
    - using `asyncio.sleep` for busy waiting is discouraged to avoid unnecessary events & commands
### How To Send Signals
- `temporalio.client.WorkflowHandle.signal` is used to send signlas through client API
    - `client.Client.start_workflow`
    - `client.Client.get_workflow_handle`
    - `client.Client.get_workflow_handle_for`
- `temporalio.workflow.ExternalWorkflowHandle.signal` is used to send signals from within workflow executions
    - `get_external_workflow_handle`
    - `get_external_workflow_handle_for`
### Signal With Start
- using `start_signal` & `start_signal_args` parameters `temporalio.client.Client.start_workflow`
- used to check if workflow execution exists & if not, start it & then send it given signal
### Common Problems With Signals & Their Workarounds
- number of outgoing pending signals per workflow execution is limited to 2000
- number of received signals per workflow execution is limited to 10000
### What Is The Entity Workflow Pattern
- problem
    - order of signals & handling them is important
    - number of signals is high
    - handling signals concurrently will break determinism
- solution
    - queue mechanisms like `asyncio.Queue` are used to preserve order of signals
    - execution results of child workflows are awaited before launching new executions
## Querying Your Workflows
### What Are Queries?
- used to get information about internal state of open or closed workflow executions
- useful for monitoring workflow executions & getting activity results without invoking them directly
- shouldn't mutate state of workflow executions & won't create event history commands (keeps workflow executions deterministic)
- are read only & executed synchronously
### Developing Queries
- queries are executed by workers which handle givne workflow & are polling from the same task queue on which given execution happend
- query type is used to identify queries on both ends (clients & workflow definitions)
- `temporalio.workflow.query` is used to define query handlers on workflow definition classes
- query handlers can receieve parameters (must be serializable)
### Sending A Query With The SDK
- `temporalio.client.WorkflowHandle.query` is used to send queries through client API
### Daynamic Queries
- dynamic query
    - `dynamic` parameter is set to `True` when using `temporalio.workflow.query`
    - invoked dynamically at runtime when no other query with the given name is defined
- dynamic signals
    - `dynamic` parameter is set to `True` when using `temporalio.workflow.signal`
    - invoked dynamically at runtime when no other signal with the given name is defined
- these should accepts self, name & parameters as `collections.abc.Sequence[temporalio.common.RawValue]`
- `temporalio.workflow.payload_converter` can be used to deserialize parameters
## Workflow Cancellation
### What Is An Activity Heartbeat
- periodic ping sent by activities to temporal cluster, in order to
    - indicate progression
    - provide worker health check
    - cancellation detection
- heartbeat timeout is the maximum time between activity heartbeats
### Cancelling VS Terminating Workflow Executions
- cancelling workflow executions
    - is graceful & allows clean up operations
    - causes workflow task to be scheduled in order to handle the cancellation
    - allows workflow execution to respond to cancellation request
- terminating workflow executions
    - is forceful & shuts down executions
    - running activities are cancelled & corresponding workers will be notified upon the next activity heartbeat
- workflow executions are terminated by temporal cluster upon reaching limits
### Handling Workflow Cancellation
- handling code of cancellation request in workflow execution is written inside `finally` block
- behaviour of blocking activities upon cancellation is specified by setting `cancellation_type` when calling them
- workflow execution status after cancellation request will be
    - complete: if all activities greacefully handle cancelation request
    - canceled: otherwise
### Cancelling An Activity From A Workflow
- activities must regularly send heartbeats to temporal cluster in order to be cancellable
- cancellastion requests are given to activities by temporal cluster in response to their heartbeat (?) 
- [local activities](https://docs.temporal.io/local-activity) can be cancelled even if they don't send heartbeats
- `except asyncio.CancelledError` is raised in activities in order to indicate cancellation request & is caught to greacefully clean up
## Asynchronous Activity Completion
### What is Asynchronous Activity Completion?
- enables keeping status of activities open or in progress after their function is returned
- the activity will have to send heartbeath to temporal cluster after returning
### When To Use Asynchronous Completion
- methods of informing temporal cluster with completion result of activity execution by external systems
    - asynchronous completion by the external system
        - external system directly informs temporal cluster
        - process is started by activity & completion result is reported back by external system
        - useful for long running processes
    - signal from the external system: completion result is sent as signal to the workflow by the external system
    - polling by subsequent activity: completion result is polled from the external service by subsequent activities
### Deciding Between Asynchronous Completion & Signals
- asynchronous completion is useful when
    - the external system is unreliable
    - activity heartbeats are needed (for monitoring)
- using signals are useful when
    - the external system is reliable
    - activity heartbeats & continuous monitoring aren't needed
- typically require long start to close timeout
### How to Asynchronously Complete Activities
- task tokens are used to track activity executions
- `temporalio.activity.info` is used to access task token
- `temporalio.activity.raise_complete_async` is used to inform temporal cluster that activity is being carried by the external system
- `temporalio.activity.hearbeat` is used to send heartbeats to temporal cluster
- `temporalio.client.Client.get_async_activity_handle` is used to acquire instance of `temporalio.client.AsyncActivityHandle` corresponding to the activity
- `temporalio.client.AsyncActivityHandle.complete` is used to notify temporal cluster about activity completion
- `temporalio.client.AsyncActivityHandle.fail` is used to notify temporal cluster about activity failure