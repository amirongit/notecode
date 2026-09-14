# RabbitMQ
## Getting started
a message broker accepts & forwards messages.<br>
messages are in the form of binary blobs.<br>
queues are large hardware-bounded buffers in which messages are stored.<br>
senders & recievers may use queues.<br>
these components do not have to reside on the same host.

RabbitMQ supports multiple messaging protocols, i.e. AMQP.<br>
[`pika`](https://github.com/pika/pika) is recommended for python applications to work with RabbitMQ over AMQP.<br>
it has an extremely trouble & non-pythonic interface, like a total piece of shit which should be wrapped with maximum care.<br>
[`kombu`](https://github.com/celery/kombu) is a way better option.

messages are distributed among recievers in a round-robin manner.<br>
acknowledgements are sent by recievers to mark messages as processed & deletable.<br>
unacknowledged messages are redelivered to recievers upon delivery acknowledgement timeouts.

durable queues survive node restarts & crashes.<br>
durable messages can be sent to durable queues in order to be persisted & survive node restarts & crashes.<br>
durable messages do not guarantee persistence by themselves, since the node could crash after accepting the message & before persisting it.

it is possible to specify the number of pre-fetched messages for recievers.<br>
this is used distribute messages based on how busy recievers are.

publisher-subscriber, in contrast to the producer-consumer pattern, is used to deliver a single message to multiple receivers.<br>
receivers are able to declare temporary & fresh queues & bind them to exchanges, which are deleted upon disconnection using the `exclusive` flag.<br>
senders use exchanges rather than sending messages directly to queues.<br>
exchanges are responsible for taking & pushing messages to their bound queues.<br>
exchanges may discard or append recieved messages to one or multiple queues.

bindings relate queues to exchanges with a routing key, whose value is used for different purposes based on the exchange type.<br>
it is possible to bind the same queues & exchanges with different routing keys.<br>
it is possible to bind different queues to the same exchange with the same routing key.<br>
routing keys are specified by senders as an attribute of messages.<br>
it is possible to specify multiple routing keys for a message.

RPC calls are implemented using the `[reply_to, correlation_id]` properties defined in AMQP.<br>
in the context of RPC, clients declare temporary callback queues & use them as the `reply_to` property to receive responses.<br>
the `correlation_id` property is set to a unique value for each request message & used to find its response within the callback queue.

[`rstream`](https://github.com/rabbitmq-community/rstream) is recommended for python applications to work with RabbitMQ streams.
## How to use RabbitMQ
RabbitMQ is a messaging broker, which accepts, routes, stores (& removes), & delivers messages.<br>
senders usually have long life spans because of the cost of opening connections & sessions.

[*protocol differences*](https://www.rabbitmq.com/docs/publishers#protocols)<br>
all the protocols support messages, payloads, headers & acknowledgement mechanisms.

exchanges are named routing tables declared by applications.<br>
bindings associate streams, queues or other exchanges to these routing tables.<br>
exchanges may be durable or transient.<br>
built-in exchange types are
- default: routes based on queue names & message routing keys
- topic: routes based on binding patterns & message routing keys
- fanout: does broadcasting
- direct: routes based on exact binding & message keys
- local random
- modulus hash
- JMS topic
- consistent hash
- random
- recent history
- headers

one exchange per type is pre-declared using the name of its type.<br>
alternate exchanges allow delegation of routing to other exchanges.

publisher confirm is an acknowledgement mechanism between senders & nodes to ensure data-safety.<br>
strategies to use publisher confirm are
- streaming confirms: messages are managed asynchronously
- batch publishing: messages are managed in batches
- publish & wait: messages are managed individually

[*recovery from connection failures*](https://www.rabbitmq.com/docs/publishers#connection-recovery)

[*concurrency considerations*](https://www.rabbitmq.com/docs/publishers#concurrency)

receivers usually have long life spans because of the cost of opening connections & sessions.<br>
[*connection recovery*](https://www.rabbitmq.com/docs/consumers#connection-recovery)<br>
they are registered by applications on queues & identified by consumer tags.<br>
acknowledgement method of receivers may be automatic or manual, which is specified upon instantiation.<br>
receivers are cancelled using their consumer tags to stop receiving messages.<br>
receivers may be used to implement pull or push based messaging.<br>
exclusive receivers are the only receivers of their associated queues.

single-active-consumer is used to enforce one active consumer at a time for a given queue.<br>
this enables processing messages while preserving their order.<br>
this attribute may be set on queues upon declaration.<br>
SAC & exclusive receivers are mutually exclusive.

receiver priority is used to ensure that high priority receivers are delivered messages when it is possible to.<br>
low priority receivers will receive messages when high priority ones are busy or not active.

[*concurrency considerations*](https://www.rabbitmq.com/docs/consumers#concurrency)

<!-- https://www.rabbitmq.com/docs/consumer-cancel -->
