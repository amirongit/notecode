# What Is Temporal?
## Introducing Temporal
### What Is Temporal?
- platform to guarantee durable execution
- enables applications to run reliably even while encountering failures
    - I/O outage
    - server crash
    - application crash
- removes need for writing application code which handles & recovers from mentioned failures
### Workflows
- abstraction used to build temporal applications
- resilient
- developed using general purpose programming languages
- are able to recreate pre failure state of applications in case of failure
## What Is A Workflow?
### A Sequence Of Steps
- workflows define sequences of steps (using code)
- code used to define workflows is called "workflow definition"
- executing workflows result in "workflow execution"s
## Workflow Examples
### Expense Report
- common characteristics
    - long running
    - conditional branches
    - cycles
    - human interactions
    - third party system interactions
### Money Transfer
- workflows could be composed of other workflows
- remotely calling procedures makes systems "distributed" (in broader senses thogh!)
- temporal workflows are able to track state between multiple systems, thus, provide possibility of
    - defining atomic transactions
    - rolling them back
## Architectural Overview
### Temporal Server
1. temporal server
    - necessary components to execute applications durably
    - frontend service which also acts as API gateway (used by clients)
    - horizontally scalable
    - communications happen using gRPC & protobuf (using TLS is possible)
2. its clients
    1. CLI
    2. web UI
    3. embedded application client
3. data stores
    1. relational, used to
        - track state of executions
        - store events & relatable details
        - other information like queues & timers
    2. elasticsearch (optional): provides advanced searching, sorting & filtering
4. prometheus (optional): used to collect metrics
5. grafana (optional): used in conjunction with prometheus to create dashboards in order to monitor clusters & applications
### Workers
- applications contain code to initialize workers, workflows & domain logic
- workers are responsible to
    1. execute application code
    2. communicate with temporal server through frontend service using embedded clients to manage execution of workflows
- temporal is just responsible for reliability & durability
    - does it through orchestration
    - doesn't even have access to application code
## Temporal Command Line Interface: `temporal`
### What Is `temporal`?
- command line interface for temporal which allows communication with cluster
# Developing A Workflow
## Writing A Workflow Definition
- workflow type: name assigned to each workflow
## Input Parameters & Return Values
### Values Must Be Serializable
- inputs & outputs of workflows & activities must be serializable
- temporal enforces this constraint in order to be able to track state of workflows
### Data Confidentiality
- it is possible to write custom data converters
- data converters can be used to encrypt & decrypt data upon entering & exiting temporal cluster
## Initializing The Worker
### The Role Of A Worker
- usually provided by SDK
- execute workflow code
- configured, embedded & executed by application
- establishes persistent connection to cluster
- begins long polling task queue, seeking work to perform (orchestrated by cluster)
### Initializing A Worker
- configured using three components
    1. temporal client: used for communication with cluster
    2. task queue name: maintained by temporal server
    3. workflow definition: used to bind with workflow
### The Lifetime Of A Worker
- isn't bound to workflow execution
- workflow executions aren't necessarily done by one single worker
- workers are able to pick up workflow executions from where another worker failed
### Choosing Names For Task Qeues
- names are case sensitive
# Executing A Workflow
## Executing A Workflow From The Command Line
### Using `temporal` To Start A Workflow
```bash
temporal workflow start --type <workflow-type> --task-queue <task-queue> --workflow-id <workflow-execution-id> --input <input> --address <frontend-address>
```
# Viewing Workflow Execution History
## Viewing Workflow Execution History With The Temporal CLI
### Running `temporal workflow show`
```bash
temporal workflow show --workflow-id <workflow-execution-id> --address <frontend-address>
```
- `--detailed` could be used to produce more detailed result
# Modifying An Existing Workflow
## Making Changes To A Workflow
- backwards compatibility is important consideration in workflow definitions
- when workflows fail, their state is reconstructed within current version
### Input Parameters & Return Values
- number of parameters should not be changed
- dataclasses are suitable options because they enable adding optional arguments without changing types of arguments of workflows
### [Determinism](https://docs.temporal.io/workflow-definition#deterministic-constraints)
- given same input, workflows must produce same output & perform same steps (including invocation of other workflows)
- this implies that workflow definitions should not perform I/O bound tasks directly
### Versioning
- SDK feature which enables changing workflow definitions non deterministically
- enables new executions to use latest workflow definition while older executions will be using older one(s)
## Restarting The Worker Process
- required for new changes to take effect
# [Workflow Sandbox](https://github.com/temporalio/sdk-python?tab=readme-ov-file#workflow-sandbox)
- workflows get executed & resumed inside sandboxes in order to avoid non deterministic code
    - this ensures isolation of workflow executions & their context
    - it is encouraged to have workflow definitions in separate files to avoid side effects
- if non deterministic code is performed, an exception is raised
## How Does The Sandbox Work?
1. global state isolation (achieved through python's builtin `exec` function)
2. restrictions to prevent known non deterministic library calls (python SDK implementes its own custom importer (achieved by re implementing [importlib](https://docs.python.org/3/library/importlib.html)))
## Avoiding The Sandbox
1. `temporalio.workflow.unsafe.sandbox_unrestricted` is used to remove restrictions for code blocks
2. `sandboxed` parameter of `workflow.defn` is set to `False` to avoid workflows being executed inside sandbox
3. instance of `temporalio.worker.UnsandboxedWorkflowRunner` is passed to `workflow_runner` parameter of `Worker` class in order to disable sandbox for given worker
## Pass Through Modules
- used to exclude activities & desired non deterministic code from sandbox & being imported on workflow definition loads
- makes marked modules to be used directly from outside of sandbox
- possible because of custom import system
- it is encouraged to mark all known deterministic side effect free code as pass through to avoid repetitive & expensive imports
### Marking Modules As Pass Through
1. `temporalio.workflow.unsafe.imports_passed_through` is used to mark imports as pass through
2. `SandboxRestrictions.default.with_passthrough_modules(<modules>)` is passed to `restrictions` parameter of `SandboxedWorkflowRunner` which is passed to `workflow_runner` parameter of `Worker` class to mark specified modules as pass through at sandbox level
3. `SandboxRestrictions.default.with_passthrough_all_modules()` is passed to `restrictions` parameter of `SandboxedWorkflowRunner` which is passed to `workflow_runner` parameter of `Worker` class to mark all modules as pass through at sandbox level
# Developing An Activity
## What Are Activities?
- activities are used to encapsulate sequences of steps that are prone to failure (therefore, non deterministic)
- executed as part of workflow definitions
- their execution is retried if failed
- activities are execution points from where failed workflow executions pick up & continue to perform other steps
## Registering Activities
- activities should also be bound to wokers in order to get executed
## Executing Activities
### Importing Moduels Into Workflow Files
- since activities could be non deterministic, they are marked as pass through
### Specifying Activity Options
- custom wrappers in SDK is used to execute activities
- this allows temporal cluster to detect crashed workers, set options like timeout, scheduling & etc...
### Retrieving The Result
- workflows don't execute activity
- using wrappers, workflows request execution of activities to temporal cluster
- wrappers named `execute...` are synchronous; therefore, they block & return activity results when possible
- wrappers named `start...` are asynchronous
    - they request execution of activities to temporal cluster & return handlers without furthur blocking
    - returned handlers could be awaited in order to get results of wrapped activities
## Using Appropriate Timeouts
- high value for timeouts delay this detection of crashed workers because this is how temporal cluster does it
# Handling Activity Failure
## How Temporal Handles Activity Failure
- temporal retries failed activities (with short delays between each attempt) untill succession or cancelation (by reaching maxium attempts or maximum interval)
- attempts, intervals are configurable using dedicated SDK parameters
