"""Lab 01-12: Evaluator–Reviser 패턴의 제한된 반복을 확인합니다.

시나리오:
    Writer Agent가 안내 문장을 작성하고 Evaluator Agent가 필수 안전 문구를 검사합니다.
    기준을 통과하지 못하면 Reviser가 문장을 수정한 뒤 다시 평가합니다. 반복 횟수는
    Python이 최대 5회로 제한하며 Evaluator가 통과시키거나 한도에 도달하면 종료합니다.
    기준을 일찍 통과하면 남은 횟수를 모두 실행하지 않고 즉시 종료합니다.

학습 질문:
    생성 Agent와 평가 Agent의 기준을 분리하면 어떤 장점이 있으며, 반복은 누가
    멈춰야 할까요?

범위:
    Evaluator와 Reviser는 실제 LLM을 사용합니다. 필수 문구 최종 판정과 최대 5회
    종료는 Python이 결정적으로 보장합니다.
"""

from shared.travel_contracts import EvaluationResult
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


REQUIRED_TEXT = "승인 전에는 결제를 실행하지 않습니다."


def writer_agent(request: str) -> dict:
    return run_learning_agent("writer_agent", "사용자 요청에 맞는 여행 예약 안내 초안을 작성한다.", request)


def evaluator_agent(draft: str) -> dict:
    prompt = f"""당신은 evaluator_agent입니다.
초안에 다음 필수 문구가 정확히 포함됐는지 평가하세요: {REQUIRED_TEXT}
초안: {draft}
EvaluationResult 계약으로 반환하세요."""
    response = run_with_metadata(provider_for_agent("evaluator_agent"), prompt, EvaluationResult)
    if response["result"] is not None and REQUIRED_TEXT not in draft:
        response["result"]["passed"] = False
        response["result"]["feedback"] = "필수 안전 문구를 정확히 추가하세요."
        response["result"]["missing_requirements"] = [REQUIRED_TEXT]
    return response


def reviser_agent(draft: str, feedback: str) -> dict:
    goal = f"평가 의견을 반영해 초안을 수정하고 다음 문구를 정확히 포함한다: {REQUIRED_TEXT}"
    return run_learning_agent("reviser_agent", goal, draft, feedback)


def review_loop_orchestrator_agent(request: str, max_rounds: int = 5) -> dict[str, object]:
    trace = []
    writer_result = writer_agent(request)
    trace.append({"step": "writer", "provider": writer_result["provider_requested"], "error": writer_result["error"]})
    if writer_result["error"]:
        return {"status": "failed", "reason": "writer_failed", "draft": None, "trace": trace}
    draft = writer_result["result"]["summary"]

    for round_number in range(1, max_rounds + 1):
        evaluation = evaluator_agent(draft)
        trace.append({"round": round_number, "actor": "evaluator_agent", "provider": evaluation["provider_requested"], "result": evaluation["result"], "error": evaluation["error"]})
        if evaluation["error"]:
            return {"status": "failed", "reason": "evaluator_failed", "draft": draft, "trace": trace}
        if evaluation["result"]["passed"] and REQUIRED_TEXT in draft:
            return {"status": "completed", "draft": draft, "trace": trace}
        if round_number == max_rounds:
            break
        revision = reviser_agent(draft, evaluation["result"]["feedback"])
        trace.append({"round": round_number, "actor": "reviser_agent", "provider": revision["provider_requested"], "error": revision["error"]})
        if revision["error"]:
            return {"status": "failed", "reason": "reviser_failed", "draft": draft, "trace": trace}
        draft = revision["result"]["summary"]
    return {"status": "failed", "reason": "max_rounds", "draft": draft, "trace": trace}


if __name__ == "__main__":
    result = review_loop_orchestrator_agent("승인 전 결제를 실행하지 않는 여행 예약 안내문을 작성해 주세요.")
    print(result)
    print("반복 완료:", result["status"] == "completed")
    print("필수 문구 포함:", bool(result["draft"]) and REQUIRED_TEXT in result["draft"])
    print("설정된 최대 반복 횟수:", 5)
    evaluation_count = sum(1 for event in result["trace"] if event.get("actor") == "evaluator_agent")
    print("실제 평가 횟수:", evaluation_count)
    print("통과하면 최대 반복 전에 조기 종료:", evaluation_count < 5)
