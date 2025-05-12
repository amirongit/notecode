# NATS docs
## Core NATS
### NATS Concepts
#### What Is NATS?
##### What is NATS?
message oriented middleware which allows applications to exchange data. unit of data is called message
##### NATS service infrastructure
one or more NATS server processes that are configured to interconnect with each other
##### QoS (quality of service)
is the description or measurement of the overall performance of a service, particularly the performance seen by the users of the network
##### NATS QoS
- core NATS
    - offers at most once QoS, meaning that if there isn't a subscriber listening on a particular subject, or isn't active when messages are sent, messages are discarded
- NATS jetstram
    - offers at least once & exactly once QoS
#### Subject-Based Messaging
##### Interest based messaging
when using this method of messaging, listeners have to subscribe to subsets of subjects in order to recieve messages published on them
##### Subject
named communication channels for publishing & listening for messages; made on top of an string of characters that form a name which is used by publishers & subscribers to find each other
##### Subject hierarchies
`.` is used to create a subject hierarchy; publishers should specify the exact subject when publishing messages while subscribers have the ability to listen to hierarchies
##### Wildcards
can take the place of one or more elements in a subject hierarchy
- `*`
    - matches exactly one single whole token & can be used multiple times
- `>`
    - matches one or more tokens & appears at the end of the name of the subject
