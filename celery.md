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

configurations are accessed through `<app>.conf` & applied either directly or using `<instance>.conf.[update, config_from_object, config_from_envvar]`.<br>
configurations are consulted in this order
- runtime changes
- configuration objects
- defaults

[*laziness*](https://docs.celeryq.dev/en/stable/userguide/application.html#laziness)

tasks decorated by `<instance>.task` will be instances of `celery.Task` by default.<br>
the base class for tasks may be customized through the `base` argument of `<instance>.task`, `<instance>.Task` or `task_cls` upon app instantiation.
### Tasks
task instances wrap callables, defining the logic of calling & processing the task.<br>
calling & processing tasks happens through sending & receiving messages, respectively.<br>
tasks have unique names, used as references in messages & by workers for resolving functions.

task messages are kept in queues until acknowledged by workers.<br>
by default, this happens before task execution to ensure a single call.<br>
this behavior may be customized & paired with idempotent tasks.<br>

task messages are also acknowledged in case of terminated executions.<br>
this behavior may be customized.

tasks are declared using `[<instance>.task, celery.shared_task]`.<br>
bound tasks pass themselves as the first argument to their associated callable.

`celery.Task.retry` is used for re-execution by tasks themselves.<br>
this will usually raise `celery.exceptions.Retry` for state management purposes.<br>
raising the exception can be disabled through the `throw` argument.<br>
`exc` argument is used to pass exception information for logs & results.<br>
if the task maximum retries is reached, either `exc` or `celery.exceptions.MaxRetriesExceededError` is raised.<br>
retrying will affect task status.

`default_retry_delay` argument is used upon task declaration to specify the default retry delay.<br>
`countdown` argument of `celery.Task.retry` takes precedence.<br>
`autoretry_for` argument is used upon task declaration to specify exceptions on which the task should be retried.

[*list of options*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#list-of-options)<br>
[*states*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#states)

[*result backends*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#result-backends)<br>
backends may use resources to store results.<br>
`celery.result.AsyncResult.[get, forget]` will release the resources.

[*ignore*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#ignore)<br>
[*reject*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#reject)

task handlers are methods executed synchronously at specific points in a task's lifecycle.
|#|name|desc|overridable|
|-|-|-|-|
|1|`before_start`|does preparation & its return value is ignored|+|
|2|`run`|executes the associated callable|-|
|3|`[result backend]`|persists task state & its return value|-|
|4|`[on_success, on_retry, on_failure]`|-|+|
|5|`after_return`|called for terminal states (skipped for RETRY, RJECED, IGNORED)|+|

[*requests & custom requests*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#requests-and-custom-requests)

[*how it works*](https://docs.celeryq.dev/en/stable/userguide/tasks.html#how-it-works)
<!-- https://docs.celeryq.dev/en/stable/userguide/calling.html -->
