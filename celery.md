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
the task base class may be customized through the `base` argument of `<instance>.task` or `<instance>.Task`.
