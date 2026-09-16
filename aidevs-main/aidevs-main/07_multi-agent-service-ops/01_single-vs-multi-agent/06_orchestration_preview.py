"""Lab 01-6: 여러 독립 Agent와 Orchestration이 아닌 구조를 확인합니다.

시나리오:
    Weather Agent와 Budget Agent가 각각 결과를 반환합니다. 두 Agent 사이에는 결과
    전달이 없고 전체 상태와 종료 조건도 없습니다. 뒤쪽 비교 함수에서는 Coordinator가
    최소한의 선택·결과 수집·종료를 담당하면 무엇이 달라지는지 확인합니다.

학습 질문:
    여러 Agent를 한 파일에서 호출했다는 사실만으로 Orchestration이라고 할 수 있을까요?

범위:
    Agent 결과는 실제 LLM이 만들고 Python은 선택·수집·종료 차이만 보여줍니다.
"""

from shared.travel_llm import run_learning_agent


def weather_agent(request: str) -> dict:
    return run_learning_agent("weather_agent", "날씨 준비 사항을 정리한다.", request)


def budget_agent(request: str) -> dict:
    return run_learning_agent("budget_agent", "예산 조건을 정리한다.", request)


AGENTS = {
    "weather_agent": weather_agent,
    "budget_agent": budget_agent,
}


def run_independently(request: str) -> list[dict]:
    """Agent가 각각 실행되지만 선택·종합·전체 종료 주체는 없습니다."""
    return [agent(request) for agent in AGENTS.values()]


def orchestrate(request: str) -> dict[str, object]:
    """Coordinator가 필요한 Agent, 실행 결과, 전체 종료를 관리합니다."""
    selected = ["weather_agent", "budget_agent"]
    trace = ["supervisor:selected:weather_agent,budget_agent"]
    results: dict[str, dict] = {}

    for agent_id in selected:
        trace.append(f"started:{agent_id}")
        results[agent_id] = AGENTS[agent_id](request)
        if results[agent_id]["error"]:
            trace.append(f"failed:{agent_id}")
        else:
            trace.append(f"completed:{agent_id}")

    failed_agents = [name for name in selected if results[name]["error"]]
    status = "failed" if failed_agents else "completed"
    summary = None if failed_agents else " / ".join(str(results[name]["result"]) for name in selected)
    trace.append(f"orchestrator:{status}")
    return {
        "status": status,
        "selected_agents": selected,
        "failed_agents": failed_agents,
        "results": results,
        "summary": summary,
        "trace": trace,
    }


if __name__ == "__main__":
    request = "부산 여행의 날씨와 예산을 확인해 줘."
    independent = run_independently(request)
    coordinated = orchestrate(request)

    print("\n여러 독립 Agent 결과:", independent)
    print("전체 상태와 종료 이유: 없음")
    print("\nOrchestration 결과:", coordinated)

    print("독립 Agent 수가 2개:", len(independent) == 2)
    print("선택 Agent 확인:", coordinated["selected_agents"] == ["weather_agent", "budget_agent"])
    print("전체 실행 상태:", coordinated["status"])
    print("실패 Agent:", coordinated["failed_agents"])
    print("종료 Trace 확인:", coordinated["trace"][-1] == f"orchestrator:{coordinated['status']}")
    print("확인: Orchestration은 Agent 수가 아니라 선택·전달·상태·종료를 관리합니다.")
