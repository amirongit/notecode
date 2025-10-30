# Interacting With Workflows In Python
## Signaling Your Workflows
### What Are Signals?
- asynchronously sent messages to open workflows
- used to change state or flow of workflows
- suitable for workflows that should react to external events
### Developing Signals
- steps for adding support for signals in workflows
    1. defining the signal: specifying name & data structure of the signal
    2. handling the signal: developing code that will be invoked when the signal is received
<!-- developing signals -->
