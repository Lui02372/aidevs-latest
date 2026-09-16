"""Lab 03-04: 실제 GPT Supervisor가 현재 State를 보고 다음 행동을 한 번 결정합니다.

시나리오:
    사용자 입력 검증 기능을 개발 중입니다. 요구사항 분석은 끝났지만 구현과 검토는
    남아 있습니다. Supervisor Agent는 사용자 요청과 현재 State를 읽고 다음 Worker
    또는 finish를 선택합니다.

학습 질문:
    사용자 요청만 보는 Router와 중간 State를 함께 보는 Supervisor는 무엇이 다를까요?

확인할 내용:
    Supervisor는 구현 결과를 직접 작성하지 않고 다음 행동, 지시, 전달할 Context Key와
    이유만 반환합니다. 실제 GPT를 1회 호출합니다.
"""

import json

from shared.travel_contracts import SupervisorDecision
from shared.travel_llm import provider_for_agent, run_with_metadata


def supervisor_agent(request: str, state: dict[str, object]) -> dict:
    prompt = f"""당신은 supervisor_agent입니다. Worker 업무를 직접 수행하지 마세요.
허용 순서: analyst_agent → developer_agent → reviewer_agent → finish
사용자 요청: {request}
현재 State: {state}
완료되지 않은 첫 Worker를 선택하세요. 모두 완료되었으면 finish를 선택하세요.
SupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata(provider_for_agent("supervisor_agent"), prompt, SupervisorDecision)


if __name__ == "__main__":
    current_state = {
        "completed_agents": ["analyst_agent"],
        "outputs": {"analyst_agent": "입력 길이와 허용 문자를 검증해야 합니다."},
        "current_step": 1,
        "max_steps": 4,
    }
    result = supervisor_agent("사용자 입력 검증 기능을 추가해 주세요.", current_state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["result"]:
        print("다음 Worker:", result["result"]["next_agent"])
        print("전달할 Context:", result["result"]["context_keys"])
