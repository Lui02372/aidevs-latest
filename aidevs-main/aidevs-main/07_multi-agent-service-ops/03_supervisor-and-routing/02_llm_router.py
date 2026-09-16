"""Lab 03-02: 실제 GPT Router가 담당 Worker 하나를 선택하고 선택된 Worker만 실행합니다.

시나리오:
    사용자가 "배송이 늦어서 취소하고 싶다"처럼 두 의도가 섞인 문의를 보냈습니다.
    GPT Router Agent가 현재 가장 먼저 필요한 역할을 구조화된 계약으로 선택하고,
    선택된 실제 Worker Agent만 자신의 Goal을 수행합니다.

학습 질문:
    담당 Agent를 선택하는 책임과 실제 문의에 답하는 책임은 왜 분리해야 할까요?

확인할 내용:
    Router 결과와 Worker 결과, Provider Metadata를 따로 출력합니다. 오류를 고정된 성공
    결과로 바꾸지 않습니다. 정상 흐름에서는 실제 LLM을 2회 호출합니다.
"""

import json

from shared.travel_contracts import SupportRouteDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


WORKER_GOALS = {
    "delivery_agent": "배송 상태를 확인하는 방법과 다음 행동을 안내한다.",
    "refund_agent": "환불 가능 조건과 필요한 정보를 안내하고 결제를 직접 취소하지 않는다.",
    "technical_support_agent": "로그인과 앱 오류의 해결 순서를 안내한다.",
}


def llm_router_agent(message: str) -> dict:
    prompt = f"""당신은 router_agent입니다. 직접 고객지원 답변을 작성하지 마세요.
배송 상태 확인은 delivery_agent, 환불·취소 조건은 refund_agent,
로그인·앱 오류는 technical_support_agent를 선택하세요.
담당자를 정할 수 없으면 request_information을 선택하고 필요한 정보를 작성하세요.
요청: {message}
SupportRouteDecision 계약으로 반환하고 agent_id는 router_agent로 작성하세요."""
    return run_with_metadata(provider_for_agent("router_agent"), prompt, SupportRouteDecision)


def selected_worker_agent(agent_id: str, message: str) -> dict:
    if agent_id not in WORKER_GOALS:
        raise ValueError(f"실행할 수 없는 Worker입니다: {agent_id}")
    return run_learning_agent(agent_id, WORKER_GOALS[agent_id], message)


if __name__ == "__main__":
    request = "ORDER-102 배송이 너무 늦어서 취소하고 싶습니다. 먼저 무엇을 확인해야 하나요?"
    route = llm_router_agent(request)
    print("=== Router 결정 ===")
    print(json.dumps(route, ensure_ascii=False, indent=2))
    if route["result"] is None:
        print("Router 오류로 Worker를 실행하지 않습니다.")
    elif route["result"]["selected_agent"] == "request_information":
        print("추가로 필요한 정보:", route["result"]["missing_information"])
    else:
        worker = selected_worker_agent(route["result"]["selected_agent"], request)
        print("\n=== 선택된 Worker 결과 ===")
        print(json.dumps(worker, ensure_ascii=False, indent=2))
