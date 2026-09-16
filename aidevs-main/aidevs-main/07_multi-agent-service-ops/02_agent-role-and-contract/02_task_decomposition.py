"""Lab 02-02: 사용자 업무를 Agent가 담당할 작은 Task로 분할합니다.

시나리오:
    사용자는 "부산 여행을 계획해 줘"라고 요청했습니다. 하나의 Agent가 날씨, 장소,
    예산, 안전, 일정 작성을 모두 담당하면 책임과 실패 지점을 구분하기 어렵습니다.
    먼저 업무를 작은 Task로 나누고 각 Task의 담당 Agent와 완료 조건을 정합니다.

학습 질문:
    큰 요청을 문장 길이나 Tool 개수로 나누는 것과 독립 책임으로 나누는 것은 무엇이
    다를까요?

확인할 내용:
    각 Task에는 담당 Agent, 필요한 입력, 기대 출력, 완료 조건이 있습니다. 이 단계는
    Task 설계 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from pydantic import BaseModel


class AgentTask(BaseModel):
    task_id: str
    agent_id: str
    required_input: list[str]
    expected_output: list[str]
    completion_condition: str


def task_planning_agent() -> list[AgentTask]:
    return [
        AgentTask(
            task_id="check_weather",
            agent_id="weather_agent",
            required_input=["destination", "travel_dates"],
            expected_output=["forecast_summary", "cautions"],
            completion_condition="여행 기간의 날씨와 주의사항이 정리됨",
        ),
        AgentTask(
            task_id="allocate_budget",
            agent_id="budget_agent",
            required_input=["days", "total_budget"],
            expected_output=["breakdown", "total"],
            completion_condition="항목별 금액의 합이 총예산과 일치함",
        ),
        AgentTask(
            task_id="build_itinerary",
            agent_id="itinerary_agent",
            required_input=["weather_result", "place_result", "budget_result"],
            expected_output=["day_plans", "applied_constraints"],
            completion_condition="검증된 앞 단계 결과가 일정에 반영됨",
        ),
    ]


if __name__ == "__main__":
    tasks = task_planning_agent()
    for order, task in enumerate(tasks, start=1):
        print(f"\n=== Task {order}: {task.task_id} ===")
        print(task.model_dump_json(indent=2))

    print("\n분할된 Task 수:", len(tasks))
    print("일정 Agent가 앞 결과를 필요로 함:", "budget_result" in tasks[-1].required_input)
