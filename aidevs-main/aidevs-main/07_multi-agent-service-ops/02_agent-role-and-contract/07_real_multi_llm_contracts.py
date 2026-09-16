"""Lab 02-07: 네 실제 AI Agent가 역할별 출력 계약을 지키는지 확인합니다.

시나리오:
    하나의 부산 여행 요청을 Weather, Place, Budget, Safety Agent가 각자의 관점에서
    처리합니다. 네 Agent는 Gemini, Llama, GPT, Gemma를 하나씩 사용하고 서로 다른
    Pydantic 계약으로 결과를 반환합니다.

학습 질문:
    Provider가 달라져도 Agent 사이의 출력 계약을 동일한 방식으로 검증할 수 있을까요?

확인할 내용:
    실제 Provider, Model, 지연 시간, 결과 또는 오류를 그대로 출력합니다. Provider
    실패나 계약 오류를 고정된 성공 데이터로 바꾸지 않습니다.
"""

import json

from shared.travel_contracts import BudgetResult, PlaceResult, SafetyResult, WeatherResult
from shared.travel_llm import provider_for_agent, run_with_metadata


REQUEST = "부산 2박 3일, 대중교통 이용, 총예산 60만 원, 해산물 알레르기"

AGENT_JOBS = [
    ("weather_agent", WeatherResult, "실시간 날씨 Tool을 사용하지 않았습니다. 날씨는 미확인이라고 설명하고 source_confirmed는 반드시 false로 표시하세요."),
    ("place_agent", PlaceResult, "외부 장소 Tool을 사용하지 않았습니다. 장소는 확인이 필요한 후보로 제안하고 selection_reason에 실제 운영 전 확인 필요를 명시하세요."),
    ("budget_agent", BudgetResult, "60만 원을 교통·숙박·식비·예비비로 나누고 합계를 정확히 맞추세요."),
    ("safety_agent", SafetyResult, "해산물 알레르기 위험과 확인 행동을 작성하세요."),
]


def specialist_agent(agent_id: str, schema, instruction: str) -> dict:
    prompt = f"""당신은 {agent_id}입니다.
다른 Agent의 역할을 대신하지 마세요.
사용자 요청: {REQUEST}
담당 업무: {instruction}
{schema.__name__} JSON 계약으로 반환하고 agent_id는 반드시 {agent_id}로 작성하세요."""
    return run_with_metadata(provider_for_agent(agent_id), prompt, schema)


if __name__ == "__main__":
    success_count = 0
    for agent_id, schema, instruction in AGENT_JOBS:
        response = specialist_agent(agent_id, schema, instruction)
        print(f"\n=== {agent_id} / {response['provider_requested']} / {response['model']} ===")
        print(json.dumps(response, ensure_ascii=False, indent=2))
        if response["result"] is not None:
            success_count += 1

    print(f"\n계약 검증 성공: {success_count}/{len(AGENT_JOBS)}")
    print("실패한 호출이 있다면 각 결과의 error를 확인하세요.")
