"""Lab 01-9: Router 패턴으로 필요한 Agent만 선택합니다.

시나리오:
    고객지원 서비스에 배송, 환불, 기술지원 Agent가 있습니다. 모든 문의에 세 Agent를
    실행하지 않고 GPT Router Agent가 한 Agent를 선택합니다. 선택된 실제 AI Agent만
    사용자 요청을 처리합니다.

학습 질문:
    요청마다 필요한 역할이 하나로 달라질 때 전체 Agent를 실행해야 할까요?

범위:
    구조화 계약으로 Router의 허용 Agent를 제한합니다. 상세 Routing 평가는 03에서 학습합니다.
"""

from shared.travel_contracts import LearningRouteDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


def router_agent(message: str) -> str:
    prompt = f"""당신은 router_agent입니다.
배송·택배 문의는 delivery_agent, 환불·취소 문의는 refund_agent,
로그인·기술 문제는 technical_support_agent를 선택하세요.
요청: {message}"""
    response = run_with_metadata(provider_for_agent("router_agent"), prompt, LearningRouteDecision)
    if response["error"]:
        raise RuntimeError(response["error"])
    return response["result"]["selected_agent"]


def selected_worker_agent(agent_id: str, message: str) -> dict:
    goals = {
        "refund_agent": "환불 조건을 확인한다.",
        "delivery_agent": "배송 상태 확인 방법을 안내한다.",
        "technical_support_agent": "기술 문제 해결 순서를 안내한다.",
    }
    if agent_id not in goals:
        raise ValueError(f"등록되지 않은 Agent: {agent_id}")
    return run_learning_agent(agent_id, goals[agent_id], message)


if __name__ == "__main__":
    cases = {
        "배송이 언제 도착하나요?": "delivery_agent",
        "주문을 취소하고 환불해 주세요.": "refund_agent",
        "앱 로그인이 되지 않아요.": "technical_support_agent",
    }
    for message, expected in cases.items():
        selected = router_agent(message)
        result = selected_worker_agent(selected, message)
        print(message, "→", selected, "→", result)
        print("예상 Agent 선택:", selected == expected)
