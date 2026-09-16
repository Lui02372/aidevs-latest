"""Lab 05-01: 전체 State에서 다음 Agent에 필요한 최소 Context만 선택합니다.

시나리오:
    Weather Agent가 Itinerary Agent에게 일정 조정 책임을 넘깁니다. 전체 대화와 내부
    정보가 아니라 목적지, 기간과 검증된 날씨 결과만 전달합니다.

학습 질문:
    Context를 많이 전달할수록 다음 Agent의 결과가 항상 좋아질까요?
"""

full_state = {
    "user_id": "user-101",
    "destination": "부산",
    "days": 3,
    "weather_summary": "둘째 날 비 가능성",
    "weather_cautions": ["작은 우산 준비", "실내 후보 포함"],
    "raw_messages": ["사용자의 전체 대화 원문"],
    "api_key": "절대 전달하면 안 되는 값",
    "internal_prompt": "내부 지시문",
}

ALLOWED_CONTEXT_KEYS = ("destination", "days", "weather_summary", "weather_cautions")


def minimum_context_agent(state: dict[str, object]) -> dict[str, object]:
    return {key: state[key] for key in ALLOWED_CONTEXT_KEYS if key in state}


itinerary_context = minimum_context_agent(full_state)

print("전체 key:", list(full_state))
print("전달 key:", list(itinerary_context))
print("최소 Context:", itinerary_context)
