"""Lab 05-03: YAML 경로 설정과 Python Guard로 Handoff를 검증합니다."""

from handoff_models import HandoffEnvelope
from handoff_registry import validate_handoff


def sample(**changes: object) -> HandoffEnvelope:
    data = {
        "handoff_id": "handoff-001",
        "task_id": "travel-001",
        "trace_id": "trace-001",
        "from_agent": "weather_agent",
        "to_agent": "itinerary_agent",
        "responsibility": "날씨를 반영한 일정을 만든다.",
        "context": {"destination": "부산", "days": 3, "weather_summary": "둘째 날 비"},
        "user_id": "user-101",
        "hop_count": 1,
    }
    data.update(changes)
    return HandoffEnvelope.model_validate(data)


validated = validate_handoff(sample(), expected_user_id="user-101")
print("허용: 정상 Handoff / 상태:", validated.status)

cases = [
    sample(user_id="user-999"),
    sample(from_agent="itinerary_agent", to_agent="weather_agent"),
    sample(context={"destination": "부산", "days": 3, "weather_summary": "비", "api_key": "노출 금지"}),
    sample(context={"destination": "부산"}),
]
for handoff in cases:
    try:
        validate_handoff(handoff, expected_user_id="user-101")
    except (PermissionError, ValueError) as error:
        print("차단:", error)

try:
    sample(hop_count=4)
except ValueError as error:
    print("차단: 최대 Handoff 횟수 초과")
