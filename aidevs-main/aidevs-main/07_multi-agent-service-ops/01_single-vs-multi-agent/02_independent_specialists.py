"""Lab 01-2: 독립 Goal을 가진 Specialist를 Orchestration 없이 실행합니다.

시나리오:
    Weather·Place·Budget·Safety Agent가 같은 여행 요청을 각각 처리합니다.
    GPT·Gemini·Llama·Gemma를 하나씩 배정하지만 Agent마다 독립
    Goal은 있지만 누가 실행 순서를 정하고 결과를 합치며 전체 완료를 선언하는지는
    아직 구현하지 않습니다.

학습 질문:
    Agent가 여러 개 존재하는 것과 Multi-Agent Orchestration은 무엇이 다를까요?
"""

import json
from shared.travel_contracts import SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import provider_for_agent, run_with_metadata


REQUEST = "부산 2박 3일 여행, 해산물 알레르기, 대중교통, 총예산 60만 원"
AGENTS = ("weather_agent", "place_agent", "budget_agent", "safety_agent")


def specialist_agent(agent_id: str, request: str) -> dict:
    provider = provider_for_agent(agent_id)
    prompt = f"""
당신은 {agent_id}입니다.
Goal: {SPECIALIST_GOALS[agent_id]}
다른 Agent의 역할을 대신하지 말고 자신의 결과만 SpecialistResult 계약으로 반환하세요.
실시간 Tool을 호출하지 않았으므로 확인하지 않은 사실은 missing_information에 넣으세요.
여행 요청: {request}
""".strip()
    return run_with_metadata(provider, prompt, SpecialistResult)


if __name__ == "__main__":
    results: dict[str, dict] = {}

    for agent_id in AGENTS:
        response = specialist_agent(agent_id, REQUEST)
        results[agent_id] = response
        print(f"\n=== {agent_id} ===")
        print(json.dumps(response, ensure_ascii=False, indent=2))

    succeeded = [name for name, value in results.items() if value["result"] is not None]
    failed = [name for name, value in results.items() if value["error"] is not None]
    print("성공과 실패 목록이 겹치지 않음:", set(succeeded).isdisjoint(failed))
    print("\n성공 Agent:", succeeded)
    print("실패 Agent:", failed)
    print("주의: 네 결과를 연결하거나 전체 완료를 판단하지 않았으므로 아직 Orchestration은 아닙니다.")
