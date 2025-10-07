# What Is Temporal?
## Introducing Temporal
### What Is Temporal?
- platform to guarantee durable execution
- enables applications to run reliably even while encountering failures
    - I/O outage
    - server crash
    - application crash
- removes the need for writing application code which handles & recovers from mentioned failures
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
- temporal workflows are able to track state between multiple systems, thus, provide the possibility of
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
### What Is `Temporal`?
- command line interface for temporal which allows communication with cluster
# Developing A Workflow
## Writing A Workflow Definition
- workflow type: name assigned to each workflow
## Input Parameters & Return Values
### Values Must Be Serializable
- inputs & outputs of workflows must be serializable
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
