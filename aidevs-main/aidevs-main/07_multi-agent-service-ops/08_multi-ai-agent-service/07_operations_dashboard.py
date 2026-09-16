"""
[시나리오]
운영자는 개별 Log뿐 아니라 서비스 전체 상태를 한눈에 확인해야 합니다.

1. Redis에서 현재 실행 중이거나 최근 갱신된 Task를 조회합니다.
2. PostgreSQL에서 상태별 Task 수를 집계합니다.
3. Agent별 Event 수와 실패 수를 집계합니다.
4. Dashboard가 사용할 하나의 구조화된 결과로 출력합니다.

[기대 결과]
현재 실행 수, 상태별 Task 수, Agent별 Event·실패 수가 출력됩니다.

[학습 포인트]
Dashboard는 원본 Log를 전부 보여 주는 화면이 아닙니다. 운영자가 판단할 수 있는
상태·횟수·실패 지표를 집계하고, 상세 조사가 필요할 때 task_id와 trace_id로 이동합니다.
"""

from app.repositories import PostgresHistory, RedisTasks


live_tasks = RedisTasks().active_tasks()
summary = PostgresHistory().operation_summary()
dashboard = {
    "live_task_count": len(live_tasks),
    "live_tasks": [
        {"task_id": task.task_id, "status": task.status, "progress": task.progress, "current_agent": task.current_agent}
        for task in live_tasks
    ],
    **summary,
}

print(dashboard)
