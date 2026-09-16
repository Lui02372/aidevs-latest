"""Lab 02-08: 검증된 Agent 결과만 다음 Agent의 Context로 전달합니다.

시나리오:
    GPT Budget Agent가 부산 여행 예산을 작성합니다. Python은 BudgetResult 계약 검증이
    성공한 경우에만 그 결과를 Gemma Itinerary Agent에게 전달합니다. 첫 Agent가
    실패하면 두 번째 Agent는 실행하지 않습니다.

학습 질문:
    첫 Agent가 반환한 자유 문자열을 검증 없이 다음 Agent의 Prompt에 넣으면 어떤
    문제가 생길까요?

확인할 내용:
    이 예제는 복잡한 Orchestration이 아니라 계약 경계만 다룹니다. 실제 GPT와 Gemma를
    호출하며 오류를 고정된 성공 데이터로 대체하지 않습니다.
"""

import json

from shared.travel_contracts import BudgetResult, ItineraryResult
from shared.travel_llm import provider_for_agent, run_with_metadata


REQUEST = "부산 2박 3일, 대중교통 이용, 총예산 60만 원"


def budget_agent() -> dict:
    prompt = f"""당신은 budget_agent입니다.
요청: {REQUEST}
60만 원을 교통·숙박·식비·예비비로 나누고 breakdown 합과 total을 정확히 맞추세요.
BudgetResult JSON 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("budget_agent"), prompt, BudgetResult)


def itinerary_agent(verified_budget: BudgetResult) -> dict:
    prompt = f"""당신은 itinerary_agent입니다.
요청: {REQUEST}
검증된 Budget Agent 결과: {verified_budget.model_dump_json()}
예산 항목을 반영한 3일 일정을 작성하세요. ItineraryResult JSON 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("itinerary_agent"), prompt, ItineraryResult)


def verified_result_orchestrator_agent() -> dict:
    trace = ["budget_agent:started"]
    budget_response = budget_agent()
    if budget_response["result"] is None:
        trace.append("budget_agent:contract_or_provider_failed")
        trace.append("itinerary_agent:skipped")
        return {"status": "failed", "budget": budget_response, "itinerary": None, "trace": trace}

    verified_budget = BudgetResult.model_validate(budget_response["result"])
    trace.append("budget_agent:verified")
    trace.append("itinerary_agent:started")
    itinerary_response = itinerary_agent(verified_budget)
    if itinerary_response["result"] is None:
        trace.append("itinerary_agent:contract_or_provider_failed")
        return {"status": "failed", "budget": budget_response, "itinerary": itinerary_response, "trace": trace}

    trace.append("itinerary_agent:verified")
    return {"status": "completed", "budget": budget_response, "itinerary": itinerary_response, "trace": trace}


if __name__ == "__main__":
    result = verified_result_orchestrator_agent()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\n전체 상태:", result["status"])
    print("검증된 Budget만 전달:", "budget_agent:verified" in result["trace"])
