# Celery
## Getting started
a task queue is a mechanism to distribute work across threads or machines.<br>
tasks are units of work, taken by workers for processing & monitoring.

[*bundles*](https://docs.celeryq.dev/en/stable/getting-started/introduction.html#bundles)<br>
Celery requires a message broker & optionally a result backend to function.

[*backends & brokers*](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html)<br>
Celery supports using different backends & brokers.

[*using quorum queues*](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html#using-quorum-queues)

[*configuration*](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#configuration)
## User Guide
### Application
applications are instances of `celery.Celery`, a thread-safe container object of celery components.<br>
applications & workers maintain a task registry which maps task names to their corresponding functions.

configurations are accessed through `celery.Celery.conf` & applied either directly or using `celery.Celery.conf.[update, config_from_object, config_from_envvar]`.<br>
configurations are consulted in this order
- runtime changes
- configuration objects
- defaults

[*laziness*](https://docs.celeryq.dev/en/stable/userguide/application.html#laziness)

tasks decorated by `celery.Celery.task` will be instances of `celery.Task` by default.<br>
the base class for tasks may be customized through the `base` argument of `celery.Celery.task`, `celery.Celery.Task` or `task_cls` upon app instantiation.
### Tasks
task instances wrap callables, defining the logic of calling & processing tasks.<br>
calling & processing tasks happens through sending & receiving messages, respectively.<br>
tasks have unique names, used as references in messages & by workers for resolving functions.

task messages are kept in queues until acknowledged by workers.<br>
by default, this happens before task execution to ensure a single call.<br>
this behavior may be customized & paired with idempotent tasks.<br>

task messages are also acknowledged in case of terminated executions.<br>
this behavior may be customized.

tasks are declared using `[celery.Celery.task, celery.shared_task]`.<br>
bound tasks pass themselves as the first argument to their associated callable.

`celery.Task.retry` is used for re-execution by tasks themselves.<br>
this will usually raise `celery.exceptions.Retry` for state management purposes.<br>
raising the exception can be enabled or disabled through the `throw` argument.<br>
`exc` argument is used to pass exception information for logs & results.<br>
if the task maximum retries is reached, either `exc` or `celery.exceptions.MaxRetriesExceededError` is raised.<br>
retrying will affect task status.

`default_retry_delay` argument is used upon task declaration to specify the default retry delay.<br>
`countdown` argument of `celery.Task.retry` takes precedence.<br>
`autoretry_for` argument is used upon task declaration to specify exceptions on which a task should be retried.

[*list of options*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#list-of-options)<br>
[*states*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#states)

[*result backends*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#result-backends)<br>
backends may use resources to store results.<br>
`celery.result.AsyncResult.[get, forget]` will release the resources.

built-in tasks states are
- `PENDING`
- `STARTED`
- `SUCCESS`
- `FAILURE`
- `RETRY`
- `REVOKED`

[*ignore*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#ignore)<br>
[*reject*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#reject)

task handlers are methods executed synchronously at specific points in a task's lifecycle.
|#|name|desc|overridable|
|-|-|-|-|
|1|`before_start`|does preparation & its return value is ignored|+|
|2|`run`|executes the associated callable|-|
|3|`[result backend]`|persists task state & its return value|-|
|4|`[on_success, on_retry, on_failure]`|-|+|
|5|`after_return`|called for terminal states (skipped for `RETRY`, `REJECTED`, `IGNORED`)|+|

[*requests & custom requests*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#requests-and-custom-requests)

[*how it works*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#how-it-works)
### Calling tasks
`celery.Task.apply_async` is used to schedule tasks with arguments & execution options.<br>
`celery.Task.delay` is a shortcut to `celery.Task.apply_async` without execution options.<br>
`celery.Task.__call__` is used to execute the associated callable of a task locally.

`link` argument of `celery.Task.apply_async` is used to link tasks together using their results.<br>
`errback` argument of `celery.Task.apply_async` is used to specify exception callbacks executed locally by workers.<br>
`on_message` argument of `celery.result.AsyncResult.get` is used to specify status change callbacks executed locally by workers.

`eta` (estimated time of arrival) argument of `celery.Task.apply_async` is used to specify the earliest time at which a task could be executed.<br>
`countdown` argument of `celery.Task.apply_async` is a shortcut to `eta` which accepts seconds.<br>
it is advised not to set the `eta` later than a few minutes in the future & use other solutions for more reliability.

`expires` argument of `celery.Task.apply_async` is used to specify expiration time for tasks.<br>
workers set the status of expired tasks as `REVOKED`.

[*message sending retry*](https://docs.celeryq.dev/en/stable/userguide/calling.html#message-sending-retry)

[*serializers*](https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers)

[*compression*](https://docs.celeryq.dev/en/stable/userguide/calling.html#compression)

[*connections*](https://docs.celeryq.dev/en/stable/userguide/calling.html#connections)

[*routing options*](https://docs.celeryq.dev/en/stable/userguide/calling.html#routing-options)

`[ignore_result, result_extended]` arguments of `celery.Task.apply_async` are used to enable or disable result & metadata respectively.

[*advanced options*](https://docs.celeryq.dev/en/stable/userguide/calling.html#advanced-options)
### Canvas: designing workflows
signatures are instances of `celery.canvas.Signature` which wrap task invocations without executing them.<br>
`celery.signature` & `celery.Task.[s, signature]` are used to create signatures.<br>
they implement the same calling API as tasks (`Signature.[apply_async, delay, __call__]`) for execution.

signatures may wrap task invocations incompletely, similar to `functools.partial`.<br>
additional arguments passed to `Signature.[apply_async, delay, __call__]` are prepended to the partial arguments.<br>
additional keyword arguments & execution options passed to `celery.canvas.Signature.[apply_async, delay, __call__]` are merged with the partial keyword arguments & execution options.

`celery.canvas.Signature.clone` is used to create derivatives of signatures.

`immutable` argument of `celery.signature` or `celery.Task.si` may be used to create immutable signatures.<br>
execution options of immutable signatures may still be modified.

`link` argument of `[celery.canvas.Signature, celery.Task].apply_async` is used to specify successful execution callbacks in the form of signatures.

[*the primitives*](https://docs.celeryq.dev/en/stable/userguide/canvas.html#the-primitives)<br>
primitives are signature components which may be mixed to create workflows.

`celery.group` is used to create group primitives, executing signatures in parallel.<br>
`celery.chain` or `|` are used to create chain primitives, executing signatures sequentially.<br>
`celery.chord` is used to create chord primitives, which are group primitives with a successful execution callback.<br>
`celery.Task.map` is used to create map primitives, executing signatures sequentially for each item.<br>
`celery.Task.starmap` is used to create map primitives with star-unpacked arguments, executing signatures sequentially for each tuple.<br>
`celery.Task.chunk` is used to create chunk primitives, which split items into batches & execute signatures for each batch.

[*stamping*](https://docs.celeryq.dev/en/stable/userguide/canvas.html#stamping)<br>
[*workers guide*](https://docs.celeryq.dev/en/stable/userguide/workers.html)<br>
[*daemonization*](https://docs.celeryq.dev/en/stable/userguide/daemonizing.html)<br>
[*routing tasks*](https://docs.celeryq.dev/en/stable/userguide/routing.html)<br>
[*periodic tasks*](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)<br>
[*monitoring & management guide*](https://docs.celeryq.dev/en/stable/userguide/monitoring.html)<br>
[*security*](https://docs.celeryq.dev/en/stable/userguide/security.html)<br>
[*optimizing*](https://docs.celeryq.dev/en/stable/userguide/optimizing.html)<br>
[*debugging*](https://docs.celeryq.dev/en/stable/userguide/debugging.html)<br>
[*concurrency*](https://docs.celeryq.dev/en/stable/userguide/concurrency/index.html)<br>
[*signals*](https://docs.celeryq.dev/en/stable/userguide/signals.html)<br>
[*testing with celery*](https://docs.celeryq.dev/en/stable/userguide/testing.html)<br>
[*extensions & bootsteps*](https://docs.celeryq.dev/en/stable/userguide/extending.html)<br>
[*configuration & defaults*](https://docs.celeryq.dev/en/stable/userguide/configuration.html)
