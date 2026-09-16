"""Lab 01-7: Sequential Orchestration을 가장 작은 예로 확인합니다.

시나리오:
    콘텐츠 팀이 부산 여행 안내문을 만듭니다. Research Agent가 핵심 사실을 정리하고,
    Writer Agent가 그 결과로 초안을 작성하며, Reviewer Agent가 초안을 검토합니다.
    앞 단계가 실패하면 뒤 Agent는 실행하지 않습니다.

학습 질문:
    이전 Agent의 결과가 다음 Agent의 필수 입력일 때 어떤 실행 구조가 적합할까요?

범위:
    세 실제 AI Agent를 사용하고 Python은 순서·결과 전달·실패 중단을 담당합니다.
"""

from shared.travel_llm import run_learning_agent


def research_agent(topic: str) -> dict:
    return run_learning_agent("research_agent", "안내문에 필요한 사실과 확인 항목을 조사한다.", topic)


def writer_agent(topic: str, research_result: dict) -> dict:
    return run_learning_agent("writer_agent", "조사 결과만 이용해 안내문 초안을 쓴다.", topic, research_result)


def reviewer_agent(topic: str, article: dict) -> dict:
    return run_learning_agent("reviewer_agent", "초안의 조건 누락과 과장을 검토한다.", topic, article)


def sequential_orchestrator_agent(topic: str) -> dict[str, object]:
    trace = []
    try:
        trace.append("research:started")
        facts = research_agent(topic)
        if facts["error"]:
            trace.append("research:failed")
            raise RuntimeError(facts["error"])
        trace.append("research:completed")
        trace.append("writer:started")
        draft = writer_agent(topic, facts["result"])
        if draft["error"]:
            trace.append("writer:failed")
            raise RuntimeError(draft["error"])
        trace.append("writer:completed")
        trace.append("reviewer:started")
        result = reviewer_agent(topic, draft["result"])
        if result["error"]:
            trace.append("reviewer:failed")
            raise RuntimeError(result["error"])
        trace.append("reviewer:completed")
        return {"status": "completed", "result": result, "trace": trace}
    except Exception as error:
        trace.append(f"failed:{type(error).__name__}")
        return {"status": "failed", "error": str(error), "trace": trace}


if __name__ == "__main__":
    output = sequential_orchestrator_agent("부산 여행")
    print(output)
    print("전체 완료:", output["status"] == "completed")
    print("Reviewer 결과 존재:", output.get("result") is not None)
    expected_trace = [
        "research:started",
        "research:completed",
        "writer:started",
        "writer:completed",
        "reviewer:started",
        "reviewer:completed",
    ]
    print("Trace 순서 일치:", output["trace"] == expected_trace)
