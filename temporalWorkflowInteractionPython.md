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