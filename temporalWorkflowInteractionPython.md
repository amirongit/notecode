# Interacting With Workflows In Python
## Signaling Your Workflows
### What Are Signals?
- asynchronously sent messages to open workflows
- used to change state or flow of workflows
- suitable for workflows that should react to external events
### Developing Signals
- defining the signal
    - specifying name & data structure of the signal
    - `temporalio.workflow.signal` decorator is used to define signal methods on workflow definitions
    - signal methods usually set data out of their own scope for others to access
- handling the signal
    - developing code that will be invoked when the signal is received
    - usually composed by conditions that check for their presence & the logic to handle them
    - it is encouraged to use `temporalio.workflow.wait_condition` instead of `asyncio.sleep` when awaiting signals
    - using `asyncio.sleep` for busy waiting is discouraged to avoid unnecessary events & commands
### How To Send Signals
- using temporal client
    - instance of `temporalio.client.WorkflowHandle` corresponding to the workflow is needed
        - `client.Client.start_workflow`
        - `client.Client.get_workflow_handle`
        - `client.Client.get_workflow_handle_for`
    - `<handle>.signal` is used to send signals
- from within workflows
    - instance of `temporalio.workflow.ExternalWorkflowHandle` corresponding to the workflow is needed
        - `get_external_workflow_handle`
        - `get_external_workflow_handle_for`
    - `<handle>.signal` is used to send signals
### Signal With Start
- this features enable checking if workflow exists & if not, starting it & then sending it the signal
- `start_signal` & `start_signal_args` can be used when calling `temporalio.client.Client.start_workflow` in order to signal with start
### Common Problems With Signals & Their Workarounds
- number of outgoing pending signals per workflow execution is limited to 2000
- number of recieved signals per workflow execution is limited to 10000

<!-- What Is The Entity Workflow Pattern -->