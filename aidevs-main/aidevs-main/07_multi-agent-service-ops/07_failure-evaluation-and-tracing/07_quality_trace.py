"""
[시나리오]
Supervisor, Worker, Evaluator, Reviser가 참여한 한 번의 여행 계획 실행을 추적합니다.

1. Supervisor가 Worker를 선택합니다.
2. Place Agent가 Timeout으로 실패합니다.
3. Orchestrator가 성공한 결과를 보존하고 Replan합니다.
4. Evaluator가 알레르기 조건 누락을 발견해 Feedback을 남깁니다.
5. Reviser가 수정하고 Evaluator가 다시 통과시킵니다.

[기대 결과]
Trace에서 actor, action, status, attempt, duration, 실패 원인과 Feedback을 시간순으로
확인할 수 있습니다. 최종 답변만 보지 않고 품질이 개선된 과정을 추적합니다.

[학습 포인트]
Trace는 print 문을 많이 남기는 것이 아닙니다. Task·Trace ID와 구조화된 필드를
사용해야 Agent별 지연, 실패, 평가 회차를 나중에 검색하고 비교할 수 있습니다.
"""

from shared.travel_observability import TraceEvent


events = [
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=1, actor="supervisor", action="route", status="completed", duration_ms=42),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=2, actor="weather_agent", action="get_weather", status="completed", duration_ms=180),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=3, actor="place_agent", action="search_places", status="failed", duration_ms=3000, error_type="TimeoutError"),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=4, actor="orchestrator", action="replan", status="completed", details={"kept_results": ["weather_agent"]}),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=5, actor="evaluator_agent", action="evaluate", status="failed", details={"failed_check": "allergy_kept", "feedback": "알레르기 조건을 일정에 반영하세요."}),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=6, actor="reviser_agent", action="revise", status="completed", details={"applied_feedback": "allergy_kept"}),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=7, actor="evaluator_agent", action="evaluate", status="completed", attempt=2, details={"passed": True}),
]

for event in events:
    print(event.model_dump_json())

failed = [event for event in events if event.status == "failed"]
print("\n실패 지점:", [(event.actor, event.action, event.error_type) for event in failed])
evaluation_events = [event for event in events if event.actor == "evaluator_agent"]
print("평가 횟수:", len(evaluation_events))
print("최종 평가 통과:", evaluation_events[-1].status == "completed")
