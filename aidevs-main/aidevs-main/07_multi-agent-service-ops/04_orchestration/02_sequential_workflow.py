"""Lab 04-02: 실제 AI Agent 결과를 다음 Agent 입력으로 순서대로 전달합니다.

시나리오:
    부산 소개 콘텐츠를 만들기 위해 Gemini Research Agent가 핵심 내용을 정리하고,
    GPT Writer Agent가 초안을 작성한 뒤 Gemma Reviewer Agent가 누락을 검토합니다.

학습 질문:
    앞 결과가 다음 작업의 필수 입력이라면 Agent를 동시에 실행할 수 있을까요?

확인할 내용:
    앞 Agent 결과가 성공한 경우에만 다음 Agent를 실행하고 오류가 발생하면 뒤 단계를
    Skip합니다. 정상 흐름에서는 실제 LLM을 최대 3회 호출합니다.
"""

from shared.travel_llm import run_learning_agent


STEPS = [
    ("research_agent", "부산 소개문에 필요한 검증 대상 사실과 주의할 표현을 정리한다."),
    ("writer_agent", "Research 결과만 사용해 짧은 부산 소개 초안을 작성한다."),
    ("reviewer_agent", "초안이 이전 Research 조건을 빠뜨리지 않았는지 검토한다."),
]


def sequential_orchestrator_agent(request: str) -> dict[str, object]:
    context: object | None = None
    results: dict[str, object] = {}
    trace: list[dict[str, object]] = []
    for agent_id, goal in STEPS:
        response = run_learning_agent(agent_id, goal, request, context)
        trace.append({"actor": agent_id, "provider": response["provider_requested"], "model": response["model"], "error": response["error"]})
        if response["error"]:
            return {"status": "failed", "reason": f"{agent_id}_failed", "results": results, "trace": trace}
        results[agent_id] = response["result"]
        context = response["result"]
    return {"status": "completed", "reason": "all_steps_completed", "results": results, "trace": trace}


if __name__ == "__main__":
    result = sequential_orchestrator_agent("부산을 처음 방문하는 사람을 위한 짧은 안내문을 작성해 주세요.")
    print(result)
    print("전체 상태:", result["status"])
    print("실행된 Agent:", list(result["results"]))
