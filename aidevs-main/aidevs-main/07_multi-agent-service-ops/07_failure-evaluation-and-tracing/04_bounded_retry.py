"""
[시나리오]
Weather Agent가 외부 날씨 서비스에 연결하지만 처음 두 번은 Timeout이 발생합니다.

1. Orchestrator는 Timeout을 일시적 오류로 분류합니다.
2. 같은 작업을 최대 3회까지만 Retry합니다.
3. 각 실패와 성공의 attempt 번호를 Trace에 남깁니다.
4. 셋째 시도에서 성공하면 즉시 반복을 끝냅니다.

[기대 결과]
Trace에는 failed, failed, completed 순서와 1·2·3 attempt가 출력됩니다. 최대 횟수
안에 성공하지 못하면 실패를 숨기지 않고 종료합니다.

[학습 포인트]
Retry는 동일한 작업의 일시적 실패를 다시 시도하는 것입니다. 품질 Feedback을 반영해
내용을 고치는 Reviser Loop와 다릅니다. 이 Lab은 흐름 재현용이라 외부 API를 호출하지 않습니다.
"""

from shared.travel_observability import TraceEvent


MAX_ATTEMPTS = 3
trace: list[TraceEvent] = []


def unstable_weather_service(attempt: int) -> dict[str, str]:
    # Retry 흐름을 재현하기 위한 의도적 실패이며 성공 결과를 외부 API처럼 위장하지 않습니다.
    if attempt < 3:
        raise TimeoutError("날씨 서비스 Timeout")
    return {"summary": "셋째 시도에서 응답 수신"}


for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        result = unstable_weather_service(attempt)
        trace.append(
            TraceEvent(
                task_id="travel-001",
                trace_id="trace-001",
                step=attempt,
                actor="weather_agent",
                action="get_weather",
                status="completed",
                attempt=attempt,
            )
        )
        print(result)
        break
    except TimeoutError as error:
        trace.append(
            TraceEvent(
                task_id="travel-001",
                trace_id="trace-001",
                step=attempt,
                actor="weather_agent",
                action="get_weather",
                status="failed",
                attempt=attempt,
                error_type=type(error).__name__,
            )
        )
else:
    raise RuntimeError("최대 시도 횟수 안에 복구하지 못했습니다.")

for event in trace:
    print(event.model_dump_json())
