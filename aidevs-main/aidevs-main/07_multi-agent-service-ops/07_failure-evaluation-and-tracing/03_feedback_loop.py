"""
[시나리오]
실제 AI Agent 세 개가 안전한 여행 예약 안내문을 반복해서 개선합니다.

1. OpenAI Writer Agent가 최초 안내문을 작성합니다.
2. Gemini Evaluator Agent가 필수 안전 문구와 응답 품질을 평가합니다.
3. 실패하면 OpenAI Reviser Agent가 Evaluator의 Feedback을 반영합니다.
4. 수정한 답변을 다시 Evaluator Agent가 검사합니다.
5. 기준을 통과하면 즉시 종료하고, 통과하지 못해도 최대 5회에서 종료합니다.

[기대 결과]
Trace에는 Writer, 각 회차의 Evaluator, 필요한 경우 Reviser 실행이 순서대로 출력됩니다.
통과했다면 5회를 모두 채우지 않고 조기 종료합니다. Provider 오류가 발생하면 Mock
성공으로 바꾸지 않고 failed 상태와 원인을 출력합니다.

[학습 포인트]
Feedback Loop는 같은 질문을 무한 반복하는 Retry가 아닙니다. Evaluator가 구체적인
수정 근거를 만들고 Reviser가 그 근거를 반영합니다. 반복 횟수와 최종 통과 조건은
LLM이 아니라 Python Orchestrator가 결정적으로 통제합니다.
"""

from shared.travel_contracts import EvaluationResult
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


REQUIRED_TEXT = "승인 전에는 결제를 실행하지 않습니다."
MAX_REVIEW_ROUNDS = 5


def writer_agent(request: str) -> dict[str, object]:
    return run_learning_agent(
        "writer_agent",
        "사용자 요청에 맞는 여행 예약 안내 초안을 작성한다.",
        request,
    )


def evaluator_agent(draft: str) -> dict[str, object]:
    prompt = f"""당신은 evaluator_agent입니다.
초안에 다음 필수 문구가 정확히 포함됐는지 평가하세요: {REQUIRED_TEXT}
부족한 점은 Reviser가 바로 수정할 수 있는 구체적인 Feedback으로 작성하세요.
초안: {draft}
EvaluationResult 계약으로 반환하세요."""
    response = run_with_metadata(provider_for_agent("evaluator_agent"), prompt, EvaluationResult)

    # 필수 문구 여부는 LLM 판단과 별도로 Python이 다시 보장합니다.
    if response["result"] is not None and REQUIRED_TEXT not in draft:
        response["result"]["passed"] = False
        response["result"]["feedback"] = "필수 안전 문구를 정확히 추가하세요."
        response["result"]["missing_requirements"] = [REQUIRED_TEXT]
    return response


def reviser_agent(draft: str, feedback: str) -> dict[str, object]:
    goal = f"평가 Feedback을 반영하고 다음 필수 문구를 정확히 포함한다: {REQUIRED_TEXT}"
    return run_learning_agent("reviser_agent", goal, draft, feedback)


def feedback_loop_orchestrator_agent(request: str) -> dict[str, object]:
    trace: list[dict[str, object]] = []
    writer_result = writer_agent(request)
    trace.append({"step": "writer", "provider": writer_result["provider_requested"], "error": writer_result["error"]})
    if writer_result["error"]:
        return {"status": "failed", "reason": "writer_failed", "draft": None, "trace": trace}

    draft = writer_result["result"]["summary"]
    for round_number in range(1, MAX_REVIEW_ROUNDS + 1):
        evaluation = evaluator_agent(draft)
        trace.append({"round": round_number, "actor": "evaluator_agent", "provider": evaluation["provider_requested"], "result": evaluation["result"], "error": evaluation["error"]})
        if evaluation["error"]:
            return {"status": "failed", "reason": "evaluator_failed", "draft": draft, "trace": trace}
        if evaluation["result"]["passed"] and REQUIRED_TEXT in draft:
            return {"status": "completed", "draft": draft, "trace": trace}
        if round_number == MAX_REVIEW_ROUNDS:
            break

        revision = reviser_agent(draft, evaluation["result"]["feedback"])
        trace.append({"round": round_number, "actor": "reviser_agent", "provider": revision["provider_requested"], "error": revision["error"]})
        if revision["error"]:
            return {"status": "failed", "reason": "reviser_failed", "draft": draft, "trace": trace}
        draft = revision["result"]["summary"]

    return {"status": "failed", "reason": "max_review_rounds", "draft": draft, "trace": trace}


if __name__ == "__main__":
    result = feedback_loop_orchestrator_agent("승인 전 결제를 실행하지 않는 여행 예약 안내문을 작성해 주세요.")
    print("최종 상태:", result["status"])
    print("종료 이유:", result.get("reason", "quality_gate_passed"))
    print("최종 초안:", result["draft"])
    print("최대 평가 횟수:", MAX_REVIEW_ROUNDS)
    for event in result["trace"]:
        print(event)
