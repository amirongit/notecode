# Evenet loops
# Programmin constructs or design patterns which dispatch events or messages in a program. they work by making a request
# to an event provider which usually blocks the request untill an event has arrvied and then call the relevant event
# handler. In other words, they have the ability to put tasks in a queue & put them on the call stack when it's empty.
# Event loops take unit of works (also called coroutine or a task) containing requests, event providers & event handlers
# & process them step by step concurrently.

# Coroutines
# Can be implemented using generators.
