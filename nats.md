# NATS docs
## NATS Concepts
### What Is NATS?
message oriented middleware which allows applications to exchange data. unit of data is called message
#### NATS service infrastructure
one or more NATS server processes that are configured to interconnect with each other
#### QoS (quality of service)
is the description or measurement of the overall performance of a service, particularly the performance seen by the users of the network
#### NATS QoS
- core NATS
    - offers at most once QoS, meaning that if there isn't a subscriber listening on a particular subject, or isn't active when messages are sent, messages are discarded
- NATS jetstram
    - offers at least once & exactly once QoS
### Subject-Based Messaging
#### Interest based messaging
when using this method of messaging, listeners have to subscribe to subsets of subjects in order to receive messages published on them
#### Subject
named communication channels for publishing & listening for messages; made on top of an string of characters that form a name which is used by publishers & subscribers to find each other
#### Subject hierarchies
`.` is used to create a subject hierarchy; publishers should specify the exact subject when publishing messages while subscribers have the ability to listen to hierarchies
#### Wildcards
can take the place of one or more elements in a subject hierarchy
- `*`
    - matches exactly one single whole token & can be used multiple times
- `>`
    - matches one or more tokens & appears at the end of the name of the subject
#### Pedantic mode
enables subject name verification for when messages are being published
### Core NATS
#### Publish-subscribe
##### Messages
composed of:
- subject
- byte array payload
- header fields
- optional `reply` address field
maximum size is specified in server configuration
#### Request-reply
common pattern in modern distributed systems in which request is sent & the sender either awaits the response or receives it asynchronously
### JetStream
NATS builtin persistence engine
#### Durable subscribers
type of subscribers that can receive messages published when they are inactive
#### Streaming
continuous flow of data in real-time; data is processed is it arrives under this paradigm
#### Queuing
storage of messages in a queue until they can be processed; messages are sent to a queue & processed in a usually FIFO manner
#### Replay policies
- all
    - instant
        - messages are delivered as fast as consumer can take them
    - original
        - messages are delivered at the rate they were published
- last
- starting from specific seq number
- starting from specific start time
#### Streams
message stores defining limits, discard & retention policies; consume normal NATS subjects & caputre published messages
##### Retention policies & limits
###### Limits
practical wise, streams can't grow forever; therefore limits are set
- message age
- total stream size
- number of messages in stream
- indivisual message size
- number of consumers of stream at any given time
###### Discard policies
when limits are reached & new messages are published, discard policies are applied
- discard old
- discard new
###### Retention policies
limits & discard policies always apply regardless of retention policy
- limits
    - allows replays
- work queue
    - allows exactly once consumption (for messages)
    - messages are removed as they are consumed
- ineterest
    - allows exactly once consumption (for consumers)
    - messages are removed as they are consumed by all consumers interested in the subject
##### Placement
refers to the placement of stream stream assets (data); defaults to the local cluster
can be specified using node names & tags
##### Sources & mirrors
streams configured with source or mirrors, automatically & asynchronously replicate messages from an origin stream while being able to have their own limits, discard & retention policies; also, deleting or publishing messages isn't reflected on the origin stream
- mirror
    - enables streams to source data from exactly one other stream; clients aren't allowed to write or publish messages
- source
    - enables streams to source data from multiple other streams while also allowing clients to publish messages
    - better or generalized version of mirror
##### `AllowRollUp`
if enabled, the stream will support `Nats-Rollup` header for messages which is used to indicate that all prior messages should be purged; two possible values for it are all & sub
- all
    - purges all prior messages of the stream
- sub
    - purges prior messages of the subject of the message
#### Consumers
stateful views on streams; act as an interface for clients to consume a subset of messages stored in a stream and will keep track of which messages were delivered and acknowledged by clients
##### Dispatch type
- push-based
    - messages are delivered to a specific subject
- pull-based
    - allows clients to request batchs of messages on demand
##### Persistence
- durable
- ephermal
    - doesn't persist state (in memory only)
    - is automatically cleaned up after a period of inactivity
##### `AckPolicy`
- `AckExplicit`
- `AckNone`
- `AckAll`
    - when is message is acknowledged, all previous messages are automatically done so
##### `DeliverPolicy`
- `DeliverAll`
- `DeliverLast`
- `DeliverLastPerSubject`
- `DeliverNew`
- `DeliverNew`
- `DeliverByStartSequence`
- `DeliverByStartTime`
