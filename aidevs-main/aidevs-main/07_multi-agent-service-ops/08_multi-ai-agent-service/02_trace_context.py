"""
[시나리오]
한 사용자 요청이 Backend, Worker, Supervisor, Weather Agent를 차례로 통과합니다.

1. Backend가 task_id와 trace_id를 한 번 생성합니다.
2. 각 하위 단계는 새 trace_id를 만들지 않고 같은 Trace Context를 전달받습니다.
3. 대신 자신의 순서를 나타내는 step과 actor만 변경합니다.
4. 출력된 Event를 trace_id로 묶으면 전체 실행 경로를 복원할 수 있습니다.

[기대 결과]
네 Event의 trace_id는 같고 step은 1부터 4까지 증가합니다.

[학습 포인트]
Trace는 여러 Log를 하나의 요청 경로로 연결합니다. Agent마다 trace_id를 새로 만들면
분산 실행의 전체 흐름을 찾을 수 없습니다. 이 Lab은 실제 LLM 없이 Context 전파만 봅니다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TraceContext:
    task_id: str
    trace_id: str


def create_trace_event(context: TraceContext, step: int, actor: str, action: str) -> dict[str, object]:
    return {
        "task_id": context.task_id,
        "trace_id": context.trace_id,
        "step": step,
        "actor": actor,
        "action": action,
    }


trace_context = TraceContext(task_id="task-001", trace_id="trace-001")
actors = [
    ("backend", "enqueue"),
    ("worker", "dequeue"),
    ("supervisor_agent", "route"),
    ("weather_agent", "get_weather"),
]

for step, actor_and_action in enumerate(actors, start=1):
    actor, action = actor_and_action
    print(create_trace_event(trace_context, step, actor, action))
