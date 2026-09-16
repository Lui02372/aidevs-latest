"""Lab 05-05: 거절·중복·잘못된 책임자와 대상 실패를 처리합니다.

Handoff가 실패하면 원래 Agent가 책임을 유지합니다. 같은 handoff_id를 다시 처리하거나
현재 책임자가 아닌 Agent가 Handoff를 제안하면 Python이 차단합니다.
"""

from handoff_models import HandoffEnvelope, HandoffState
from handoff_service import transfer_ownership_agent


def proposal(handoff_id: str = "handoff-001") -> HandoffEnvelope:
    return HandoffEnvelope(
        handoff_id=handoff_id, task_id="travel-001", trace_id="trace-001",
        from_agent="weather_agent", to_agent="itinerary_agent",
        responsibility="날씨를 반영한 여행 일정을 작성한다.",
        context={"destination": "부산", "days": 3, "weather_summary": "둘째 날 비"},
        user_id="user-101",
    )


if __name__ == "__main__":
    rejected_state = HandoffState(task_id="travel-001", owner_agent="weather_agent")
    rejected_state, rejected = transfer_ownership_agent(rejected_state, proposal(), False)
    print("대상 거절:", rejected.status, "/ 책임자 유지:", rejected_state.owner_agent)

    try:
        transfer_ownership_agent(rejected_state, proposal(), True)
    except ValueError as error:
        print("중복 차단:", error)

    wrong_owner_state = HandoffState(task_id="travel-001", owner_agent="budget_agent")
    try:
        transfer_ownership_agent(wrong_owner_state, proposal("handoff-002"), True)
    except PermissionError as error:
        print("잘못된 책임자 차단:", error)

    target_failure_state = HandoffState(task_id="travel-001", owner_agent="weather_agent")
    print("대상 실행 실패 전 책임자:", target_failure_state.owner_agent)
    print("수락 확인 전에는 ownership을 변경하지 않습니다.")
