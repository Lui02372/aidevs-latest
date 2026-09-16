"""
[시나리오]
Supervisor Agent가 사용자 요청을 Weather Agent에 전달했습니다. 운영자는 나중에 같은
요청에서 어떤 Agent가 무엇을 했는지 검색해야 합니다.

1. 사람이 읽는 자유 문장 대신 정해진 필드의 JSON Log를 만듭니다.
2. task_id와 trace_id로 동일한 요청의 사건을 연결합니다.
3. actor와 event로 어느 Agent가 어떤 행동을 했는지 기록합니다.
4. API Key나 전체 Prompt 같은 민감·과도한 데이터는 기록하지 않습니다.

[기대 결과]
동일한 trace_id를 가진 Supervisor와 Weather Agent Log 두 줄이 JSON으로 출력됩니다.

[학습 포인트]
Log는 최종 결과가 아니라 하나의 사건입니다. 문자열을 이어 붙이기보다 검색 가능한
구조화 필드를 사용합니다. 이 Lab은 형식 설명용이므로 실제 LLM을 호출하지 않습니다.
"""

from app.observability import structured_log


structured_log(
    "info",
    "route_completed",
    task_id="task-001",
    trace_id="trace-001",
    actor="supervisor_agent",
    details={"selected_agent": "weather_agent"},
)
structured_log(
    "info",
    "weather_completed",
    task_id="task-001",
    trace_id="trace-001",
    actor="weather_agent",
    details={"provider": "gemini", "duration_ms": 182},
)
