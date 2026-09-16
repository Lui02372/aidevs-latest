"""Lab 05-04: 대상 Agent가 수락한 뒤에만 업무 책임자를 변경합니다.

시나리오:
    Weather Agent가 Handoff를 제안했습니다. Python Guard 검증만으로 소유권을 바꾸지
    않고 Itinerary Agent가 수락한 경우에만 owner_agent를 변경합니다.
"""

from handoff_models import HandoffEnvelope, HandoffState
from handoff_service import transfer_ownership_agent


if __name__ == "__main__":
    current_state = HandoffState(task_id="travel-001", owner_agent="weather_agent")
    proposal = HandoffEnvelope(
        handoff_id="handoff-001", task_id="travel-001", trace_id="trace-001",
        from_agent="weather_agent", to_agent="itinerary_agent",
        responsibility="날씨를 반영한 여행 일정을 작성한다.",
        context={"destination": "부산", "days": 3, "weather_summary": "둘째 날 비"},
        user_id="user-101",
    )
    final_state, transferred = transfer_ownership_agent(current_state, proposal, True)
    print("Handoff 상태:", transferred.status)
    print("현재 책임 Agent:", final_state.owner_agent)
    print("Event:", final_state.events)
