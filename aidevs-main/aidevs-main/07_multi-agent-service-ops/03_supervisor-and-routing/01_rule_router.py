"""Lab 03-01: 명확한 고객지원 요청을 Python Rule Router로 분배합니다.

시나리오:
    고객지원 서비스에는 배송, 환불, 기술지원 Agent가 있습니다. 문의에 명확한 Keyword가
    있으면 LLM을 호출하지 않고 담당 Agent 하나를 선택할 수 있습니다. 정보가 모호하면
    임의로 배정하지 않고 request_information을 반환합니다.

학습 질문:
    모든 자연어 분류에 LLM Router가 필요할까요?

확인할 내용:
    Router Agent는 담당자를 선택할 뿐 고객지원 답변을 직접 작성하지 않습니다. 이
    단계는 결정적인 Routing 규칙 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from shared.travel_contracts import SupportRouteDecision


def rule_router_agent(message: str) -> SupportRouteDecision:
    routes = {
        "delivery_agent": ("배송", "택배", "도착"),
        "refund_agent": ("환불", "취소", "반품"),
        "technical_support_agent": ("로그인", "오류", "비밀번호"),
    }
    for agent_id, keywords in routes.items():
        if any(keyword in message for keyword in keywords):
            return SupportRouteDecision(selected_agent=agent_id, reason=f"{keywords} Keyword 규칙과 일치")
    return SupportRouteDecision(
        selected_agent="request_information",
        reason="담당 역할을 결정할 정보가 부족합니다.",
        missing_information=["배송·환불·기술지원 중 필요한 도움"],
    )


if __name__ == "__main__":
    messages = ["배송이 언제 도착하나요?", "주문을 환불하고 싶어요.", "로그인이 되지 않아요.", "도와주세요."]
    for message in messages:
        decision = rule_router_agent(message)
        print(f"\n요청: {message}")
        print(decision.model_dump_json(indent=2))
