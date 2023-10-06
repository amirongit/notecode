from __future__ import annotations

from queue import Queue
from select import select
from typing import Any, Generator
from uuid import UUID, uuid4


class SysCall:
    def __init__(self, *args: Any): self.args: tuple[Any, ...] = args

    def handle(self, task: Task, scheduler: Scheduler):
        raise NotImplementedError


class GetTID(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        task.send_val = task.tid
        scheduler.schedule(task)


class CreateTask(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        tid = scheduler.create(self.args[0])
        task.send_val = tid
        scheduler.schedule(task)


class KillTask(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        if (given_task := scheduler.active.pop(self.args[0], None)) is not None:
            given_task.target.close()
            task.send_val = True
        else:
            task.send_val = False
        scheduler.schedule(task)


class WaitRead(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        fd = self.args[0].fileno()
        scheduler.mark_as_pending_to_read(task, fd)


class WaitWrite(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        fd = self.args[0].fileno()
        scheduler.mark_as_pending_to_write(task, fd)


class PendTask(SysCall):
    def handle(self, task: Task, scheduler: Scheduler):
        task.send_val = scheduler.mark_as_waiting_for_other_tasks(task, self.args[0])
        if not task.send_val:
            scheduler.schedule(task)


class Task:
    def __init__(self, target: Generator):
        self.target: Generator = target
        self.tid: UUID = uuid4()
        self.send_val: Any = None

    def run(self) -> Any: return self.target.send(self.send_val)


class Scheduler:
    def __init__(self):
        self.ready: Queue[Task] = Queue()
        self.active: dict[UUID, Task] = dict()
        self.waited: dict[UUID, list[Task]] = dict()
        self.pending_to_read: dict[int, Task] = dict()
        self.pending_to_write: dict[int, Task] = dict()

    def create(self, target: Generator) -> UUID:
        task = Task(target)
        task_id = task.tid
        self.active[task_id] = task
        self.schedule(task)
        return task_id

    def schedule(self, task: Task): self.ready.put(task)

    def mark_as_done(self, task: Task):
        task.target.close()
        self.active.pop(task.tid, None)
        [self.schedule(task) for task in self.waited.pop(task.tid, list())]

    def mark_as_waiting_for_other_tasks(self, dependent_task: Task, dependee_task_tid: UUID) -> bool:
        if dependee_task_tid in self.active:
            self.waited.setdefault(dependee_task_tid, list()).append(dependent_task)
            return True
        return False

    def mark_as_pending_to_read(self, task: Task, fd): self.pending_to_read[fd] = task

    def mark_as_pending_to_write(self, task: Task, fd): self.pending_to_write[fd] = task

    def io_poll(self, timeout: int | None = None):
        if (len(self.pending_to_read) != 0) or (len(self.pending_to_write) != 0):
            i, o, _ = select(self.pending_to_read, self.pending_to_write, list(), timeout)
            for fd in i:
                self.schedule(self.pending_to_read.pop(fd))
            for fd in o:
                self.schedule(self.pending_to_write.pop(fd))

    def io_task(self):
        while True:
            if self.ready.empty():
                self.io_poll()
            else:
                self.io_poll(0)
            yield

    def loop(self):
        self.create(self.io_task())
        while len(self.active) != 0:
            task = self.ready.get()
            try:
                if isinstance((trap := task.run()), SysCall):
                    trap.handle(task, self)
                    continue
                self.schedule(task)
            except StopIteration:
                self.mark_as_done(task)
