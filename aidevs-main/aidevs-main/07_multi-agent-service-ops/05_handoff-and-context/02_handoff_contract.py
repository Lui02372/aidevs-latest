"""Lab 05-02: 책임, 추적 ID, Context 버전을 포함한 Handoff Envelope를 만듭니다."""

from pprint import pprint

from handoff_models import HandoffEnvelope


handoff = HandoffEnvelope(
    handoff_id="handoff-001",
    task_id="travel-001",
    trace_id="trace-001",
    from_agent="weather_agent",
    to_agent="itinerary_agent",
    responsibility="비 예보를 반영해 실내 대체 일정이 있는 여행 계획을 구성한다.",
    context={
        "destination": "부산",
        "days": 3,
        "weather_summary": "둘째 날 비 가능성",
        "weather_cautions": ["작은 우산 준비", "실내 후보 포함"],
    },
    user_id="user-101",
    context_version=1,
    status="proposed",
)

pprint(handoff.model_dump())
