import time

from app.repositories import PostgresHistory, RedisTasks
from app.service import append_trace, run_multi_agent
from app.observability import structured_log


def process_one(tasks: RedisTasks, history: PostgresHistory, timeout: int = 5):
    task_id = tasks.dequeue(timeout=timeout)
    if task_id is None:
        return None
    task = tasks.get(task_id)
    if task is None or task.status != "queued":
        return None
    try:
        structured_log("info", "worker_started", task_id=task.task_id, trace_id=task.trace_id, actor="worker")
        task = run_multi_agent(task)
    except Exception as error:
        task.status = "failed"
        task.error = f"{type(error).__name__}: {error}"
        append_trace(task, "worker", "orchestrate", "failed", error=task.error)
        structured_log("error", "worker_failed", task_id=task.task_id, trace_id=task.trace_id, actor="worker", details={"error": task.error})
    tasks.save(task)
    history.save(task)
    structured_log("info", "worker_finished", task_id=task.task_id, trace_id=task.trace_id, actor="worker", details={"status": task.status})
    return task


def main() -> None:
    tasks = RedisTasks()
    history = PostgresHistory()
    tasks.ping()
    history.ping()
    print("Travel Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
    while True:
        task = process_one(tasks, history)
        if task:
            print(task.task_id, task.status)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Worker를 종료합니다.")
    except Exception:
        time.sleep(1)
        raise
