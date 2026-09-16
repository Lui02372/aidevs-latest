"""Lab 04-01: Agent를 실행하기 전에 의존성이 있는 실행 계획을 검증합니다.

시나리오:
    부산 여행 계획에는 Weather, Place, Budget 조사와 Itinerary 작성이 필요합니다.
    세 Specialist는 서로 독립적이지만 Itinerary Agent는 세 결과가 모두 준비된 뒤에만
    실행할 수 있습니다.

학습 질문:
    Agent 목록만 있으면 어떤 작업을 동시에 실행하고 어디서 기다릴지 알 수 있을까요?

확인할 내용:
    PlanStep의 depends_on과 join으로 병렬 구간과 Join Barrier를 표현합니다. 이 단계는
    실행 계획 학습이므로 실제 LLM을 호출하지 않습니다.
"""

from shared.travel_orchestration import ExecutionPlan, PlanStep


def execution_plan_agent() -> ExecutionPlan:
    return ExecutionPlan(
        goal="날씨·장소·예산을 고려한 부산 2박 3일 일정 만들기",
        steps=[
            PlanStep(step_id="research", agents=["weather_agent", "place_agent", "budget_agent"]),
            PlanStep(step_id="compose", agents=["itinerary_agent"], depends_on=["research"], join=True),
        ],
        max_steps=5,
    )


if __name__ == "__main__":
    plan = execution_plan_agent()
    print(plan.model_dump_json(indent=2))
    print("\n병렬 실행 Agent:", plan.steps[0].agents)
    print("Join 뒤 실행 Agent:", plan.steps[1].agents)
    print("Compose가 Research에 의존:", "research" in plan.steps[1].depends_on)
