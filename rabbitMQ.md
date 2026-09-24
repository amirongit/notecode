# RabbitMQ
## Getting started
a message broker accepts & forwards messages.<br>
messages are binary blobs.<br>
queues are large, hardware-bounded buffers in which messages are stored.<br>
senders & receivers may use queues.<br>
these components do not have to reside on the same host.

RabbitMQ supports multiple messaging protocols, e.g. AMQP.<br>
[pika](https://github.com/pika/pika) is recommended for python applications to work with RabbitMQ over AMQP.<br>
it has an extremely troublesome & non-pythonic interface, like a total piece of shit that should be wrapped with maximum care.<br>
[kombu](https://github.com/celery/kombu) is a much better option.

messages are distributed among receivers in a round-robin manner.<br>
acknowledgements are sent by receivers to mark messages as processed & deletable.<br>
unacknowledged messages are redelivered to receivers upon delivery acknowledgement timeouts.

durable queues survive node restarts & crashes.<br>
durable messages can be sent to durable queues in order to be persisted & survive node restarts & crashes.<br>
durable messages do not guarantee persistence by themselves, since the node could crash after accepting the message & before persisting it.

it is possible to specify the number of prefetched messages for receivers.<br>
this limits the number of unacknowledged messages for receivers.<br>
this is used to distribute messages based on how busy receivers are.

publisher-subscriber, in contrast to the producer-consumer pattern, is used to deliver a single message to multiple receivers.<br>
receivers can declare temporary & fresh queues & bind them to exchanges; these queues are deleted upon disconnection using the `exclusive` flag.<br>
senders use exchanges rather than sending messages directly to queues.<br>
exchanges are responsible for taking & pushing messages to their bound queues.<br>
exchanges may discard or append received messages to one or multiple queues.

bindings relate queues to exchanges with a routing key, whose value is used for different purposes based on the exchange type.<br>
it is possible to bind the same queues & exchanges with different routing keys.<br>
it is possible to bind different queues to the same exchange with the same routing key.<br>
routing keys are specified by senders as an attribute of messages.<br>
it is possible to specify multiple routing keys for a message.

RPC calls are implemented using the `[reply_to, correlation_id]` properties defined in AMQP.<br>
in the context of RPC, clients declare temporary callback queues & use them as the `reply_to` property to receive responses.<br>
the `correlation_id` property is set to a unique value for each request message & used to find its response within the callback queue.

[rstream](https://github.com/rabbitmq-community/rstream) is recommended for python applications to work with RabbitMQ streams.
## How to use RabbitMQ
RabbitMQ is a messaging broker that accepts, routes, stores (& removes), & delivers messages.<br>
senders usually have long lifespans because of the cost of opening connections & sessions.

[*protocol differences*](https://www.rabbitmq.com/docs/publishers#protocols)<br>
all the protocols support messages, payloads, headers & acknowledgement mechanisms.

exchanges are named routing tables declared by applications.<br>
bindings are used to associate streams, queues or other exchanges to them.<br>
exchanges may be durable or transient.<br>
built-in exchange types are
- default: routes based on queue names & message routing keys
- topic: routes based on binding patterns & message routing keys
- fanout: broadcasts
- direct: routes based on exact bindings & message keys
- local random
- modulus hash
- JMS topic
- consistent hash
- random
- recent history
- headers

one exchange per type is predeclared using the name of its type.<br>
alternate exchanges allow delegation of routing to other exchanges.

publisher confirms are an acknowledgement mechanism between senders & nodes to ensure data safety.<br>
strategies for using publisher confirms are
- streaming confirms: messages are managed asynchronously
- batch publishing: messages are managed in batches
- publish & wait: messages are managed individually

[*recovery from connection failures*](https://www.rabbitmq.com/docs/publishers#connection-recovery)

[*concurrency considerations*](https://www.rabbitmq.com/docs/publishers#concurrency)

receivers usually have long lifespans because of the cost of opening connections & sessions.<br>
[*connection recovery*](https://www.rabbitmq.com/docs/consumers#connection-recovery)<br>
they are registered by applications on queues & identified by consumer tags.<br>
the acknowledgement method of receivers may be automatic or manual, which is specified upon instantiation.<br>
receivers are cancelled using their consumer tags to stop receiving messages.<br>
receivers may be used to implement pull- or push-based messaging.<br>
exclusive receivers are the only receivers of their associated queues.

single-active-consumer is used to enforce one active consumer at a time for a given queue.<br>
this enables message processing while preserving order.<br>
this attribute may be set on queues upon declaration.<br>
SAC & exclusive receivers are mutually exclusive.

receiver priority is used to ensure that high-priority receivers get messages whenever possible.<br>
low-priority receivers will receive messages when high-priority ones are busy or inactive.

[*concurrency considerations*](https://www.rabbitmq.com/docs/consumers#concurrency)

receivers may issue negative acknowledgements in order to discard or requeue messages.

queues are ordered collections of messages.<br>
queue declarations may specify length limits & TTLs.<br>
queue properties are
- name
- durable
- exclusive
- auto-delete
- [arguments](https://www.rabbitmq.com/docs/queues#optional-arguments)

message priority or redelivery may affect message delivery order.<br>
message delivery order is based on message priority & message order.

exclusive queues may only be used by the connections that declared them.

[*replicated & distributed queues*](https://www.rabbitmq.com/docs/queues#distributed)

[*CPU utilisation & parallelism considerations*](https://www.rabbitmq.com/docs/queues#runtime-characteristics)

<!-- -->
[quorum](https://www.rabbitmq.com/docs/quorum-queues#what-is-quorum) queue is a modern [raft](https://raft.github.io)-based & data-safety-oriented implementation of queues.<br>
it should be used when durability, replication & high availability are required & preferred over low latency.

[*comparison with classic queues*](https://www.rabbitmq.com/docs/quorum-queues#feature-comparison)

[*limitations*](https://www.rabbitmq.com/docs/quorum-queues#limitations)

[*delayed retry*](https://www.rabbitmq.com/docs/quorum-queues#delayed-retry)

[*features that are not supported*](https://www.rabbitmq.com/docs/quorum-queues#features-that-are-not-supported)
