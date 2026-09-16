"""Lab 01-5: Context와 Tool 권한이 역할 분리의 근거가 되는지 확인합니다.

시나리오:
    여행 서비스에서는 Weather Agent와 Budget Agent가 서로 다른 정보와 Tool을
    사용합니다. 고객지원 서비스에서는 Support Agent가 주문을 조회하고 Refund Agent만
    승인된 환불을 실행합니다. 전체 Context를 모든 Agent에게 전달하지 않습니다.

학습 질문:
    역할 이름만 나눈 것이 아니라 실제 데이터와 실행 권한도 분리됐는지 어떻게
    확인할 수 있을까요?
"""

from dataclasses import dataclass


FULL_CONTEXT = {
    "destination": "부산",
    "days": 3,
    "weather_question": "비가 오는 날이 있나요?",
    "budget": 600_000,
    "food_restriction": "해산물 알레르기",
    "payment_token": "weather_agent에게 전달하면 안 되는 값",
    "raw_messages": ["전체 대화 원문"],
}


CONTEXT_ALLOWLIST = {
    "weather_agent": {"destination", "days", "weather_question"},
    "budget_agent": {"destination", "days", "budget"},
    "place_agent": {"destination", "days", "food_restriction"},
}

TOOL_ALLOWLIST = {
    "weather_agent": {"get_weather"},
    "budget_agent": {"calculate_budget"},
    "place_agent": {"search_places"},
    "itinerary_agent": {"save_itinerary"},
}

SUPPORT_CONTEXT = {
    "user_id": "user-101",
    "question": "배송이 늦어서 환불하고 싶어요.",
    "order_id": "order-301",
    "order_status": "배송 지연",
    "refund_amount": 35_000,
    "refund_approval_id": "approval-901",
    "payment_token": "상담 Agent에게 전달하면 안 되는 값",
    "other_user_order": "다른 사용자의 주문",
}

SUPPORT_CONTEXT_ALLOWLIST = {
    "support_agent": {"user_id", "question", "order_id", "order_status"},
    "refund_agent": {"user_id", "order_id", "refund_amount", "refund_approval_id"},
}

SUPPORT_TOOL_ALLOWLIST = {
    "support_agent": {"get_order_status"},
    "refund_agent": {"execute_refund"},
}


@dataclass(frozen=True)
class AgentBoundary:
    agent_id: str
    context: dict[str, object]
    tools: set[str]


def travel_boundary_agent(agent_id: str, full_context: dict[str, object]) -> AgentBoundary:
    if agent_id not in CONTEXT_ALLOWLIST:
        raise ValueError(f"Context 규칙이 없는 Agent입니다: {agent_id}")
    allowed_keys = CONTEXT_ALLOWLIST[agent_id]
    filtered = {key: value for key, value in full_context.items() if key in allowed_keys}
    return AgentBoundary(
        agent_id=agent_id,
        context=filtered,
        tools=TOOL_ALLOWLIST[agent_id],
    )


def can_call(boundary: AgentBoundary, tool_name: str) -> bool:
    return tool_name in boundary.tools


def support_boundary_agent(agent_id: str) -> AgentBoundary:
    allowed_keys = SUPPORT_CONTEXT_ALLOWLIST[agent_id]
    return AgentBoundary(
        agent_id=agent_id,
        context={key: value for key, value in SUPPORT_CONTEXT.items() if key in allowed_keys},
        tools=SUPPORT_TOOL_ALLOWLIST[agent_id],
    )


if __name__ == "__main__":
    weather = travel_boundary_agent("weather_agent", FULL_CONTEXT)
    budget = travel_boundary_agent("budget_agent", FULL_CONTEXT)

    print("전체 Context key:", sorted(FULL_CONTEXT))
    print("Weather Context key:", sorted(weather.context))
    print("Budget Context key:", sorted(budget.context))
    print("Weather Tool:", sorted(weather.tools))

    print("Weather에 결제 Token 없음:", "payment_token" not in weather.context)
    print("Weather에 Budget 없음:", "budget" not in weather.context)
    print("Budget에 날씨 질문 없음:", "weather_question" not in budget.context)
    print("Weather Tool 허용:", can_call(weather, "get_weather"))
    print("일정 저장 Tool 차단:", not can_call(weather, "save_itinerary"))

    print("\n=== 고객 지원과 환불 비교 ===")
    support = support_boundary_agent("support_agent")
    refund = support_boundary_agent("refund_agent")
    print("Support Context:", support.context)
    print("Support Tool:", sorted(support.tools))
    print("Refund Context:", refund.context)
    print("Refund Tool:", sorted(refund.tools))

    print("Support에 승인 ID 없음:", "refund_approval_id" not in support.context)
    print("Refund에 결제 Token 없음:", "payment_token" not in refund.context)
    print("다른 사용자 주문 없음:", "other_user_order" not in support.context)
    print("Support 환불 실행 차단:", not can_call(support, "execute_refund"))
    print("Refund 환불 실행 허용:", can_call(refund, "execute_refund"))

    print("확인: 도메인이 달라도 Context와 변경 권한이 역할 분리의 근거가 됩니다.")
