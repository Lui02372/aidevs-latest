"""Lab 01-13: 실제 LLM Provider Failover를 투명하게 확인합니다.

시나리오:
    Summary Agent가 먼저 로컬 Gemma를 호출합니다. Gemma Container 또는 Model이
    준비되지 않아 실패하면 GPT를 두 번째 후보로 호출합니다. 첫 실패를 감추거나
    Mock 답변으로 바꾸지 않고 attempts에 모든 시도와 오류를 남깁니다.

학습 질문:
    Failover로 최종 응답에 성공했더라도 어떤 Provider가 먼저 실패했는지 운영자가
    확인할 수 있어야 하지 않을까요?
"""

import json

from shared.travel_llm import run_learning_agent_with_failover


def summary_agent(request: str) -> dict:
    return run_learning_agent_with_failover(
        agent_id="summary_agent",
        goal="여러 Agent 결과를 사용자가 이해하기 쉬운 세 문장으로 요약한다.",
        request=request,
        providers=("gemma", "openai"),
    )


if __name__ == "__main__":
    result = summary_agent("부산 여행 조사 결과를 세 문장으로 정리해 줘.")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("시도 횟수:", len(result["attempts"]))
    print("Failover 사용 여부:", result["failover_used"])
    print("최종 Provider:", result["provider_used"])
    print("모든 Provider 실패:", result["result"] is None)
