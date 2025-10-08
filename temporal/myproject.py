from asyncio import create_task, run, sleep
from collections.abc import Callable
from datetime import UTC, datetime
from random import choice, randint
from types import CoroutineType
from typing import Any, Awaitable, Coroutine
from uuid import uuid4

from temporalio import workflow
from temporalio.client import Client, WorkflowHandle
from temporalio.worker import Worker


@workflow.defn
class Umbrella:
    def __init__(self) -> None: ...

    @workflow.run
    async def calculate(self, dur: int | None = None) -> str:
        if dur is None:
            dur = 2
            # TODO: mark import path as pass through?!
            # dur = randint(0, 10)
        await sleep(dur)
        return f"sepehr spreaded their umbrella for {dur} seconds!"


async def create_worker(task_queue: str, client: Client) -> Worker:
    return Worker(client, task_queue=task_queue, workflows=[Umbrella])


async def execute_workflow(workflow: Any, arg: Any, task_queue: str, client: Client) -> Any:
    return await client.start_workflow(workflow, arg, id=str(uuid4()), task_queue=task_queue)  # type: ignore


async def create_client(target: str, namespace: str = "default") -> Client:
    return await Client.connect(target, namespace="default")


async def main() -> None:
    cli = await create_client("localhost:7233")
    w = await create_worker("umb-tasks", cli)

    create_task(w.run())

    while True:
        handle: WorkflowHandle = await execute_workflow(Umbrella.calculate, dur := randint(0, 9), "umb-tasks", cli)  # type: ignore
        await sleep(dur + 1)
        print(await handle.result())  # type: ignore


if __name__ == "__main__":
    run(main())
