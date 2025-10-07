from asyncio import run, sleep
from datetime import UTC, datetime
from random import randint

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@workflow.defn
class Umbrella:
    def __init__(self) -> None: ...

    @workflow.run
    async def calculate(self, dur: int | None = None) -> None:
        if dur is None:
            dur = randint(0, 10)
        await sleep(dur)
        print(f"sepehr spreaded their umbrella for {dur} seconds!")


async def main() -> None:
    cli = await Client.connect("localhost:7233", namespace="default")
    wrkr = Worker(cli, task_queue="umb-tasks", workflows=[Umbrella])
    await wrkr.run()


if __name__ == "__main__":
    run(main())
