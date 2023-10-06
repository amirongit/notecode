# Evenet loops

## What is it?

A construct or design pattern which dispatches events or messages in a program.\
it works by making a request to an event provider which usually blocks the
request untill an event has arrvied & then call the relevant event handler.\
In other words, it has the ability to put tasks in a separated queue in memory
& then put them back on the call stack when it's empty.\
Event loops take unit of works (also called coroutine or a task) containing
requests, event providers & event handlers. Then process them step by step
concurrently.
