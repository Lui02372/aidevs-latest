"""Lab 02-01: AI Agent의 역할을 실행 코드보다 먼저 정의합니다.

시나리오:
    여행 서비스에 Weather Agent와 Budget Agent를 추가하려고 합니다. 단순히 이름만
    나누면 두 Agent가 서로의 일을 대신할 수 있으므로 Goal, Responsibility, Non-goal을
    명시해 책임 경계를 먼저 만듭니다.

학습 질문:
    Agent 이름과 Prompt만 다르면 서로 다른 역할이라고 할 수 있을까요?

확인할 내용:
    Role Card에는 Agent가 달성할 목표, 해야 할 일, 하지 말아야 할 일이 함께 들어갑니다.
    이 단계는 역할 설계 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from pydantic import BaseModel


class AgentRoleCard(BaseModel):
    agent_id: str
    goal: str
    responsibilities: list[str]
    non_goals: list[str]


weather_agent_role = AgentRoleCard(
    agent_id="weather_agent",
    goal="여행 기간의 날씨 위험과 준비 사항을 정리한다.",
    responsibilities=["날씨 요약", "주의사항 작성", "출처 확인 여부 표시"],
    non_goals=["여행지 예약", "예산 변경", "결제 실행"],
)

budget_agent_role = AgentRoleCard(
    agent_id="budget_agent",
    goal="사용자 한도 안에서 여행 예산을 항목별로 나눈다.",
    responsibilities=["비용 항목 분류", "총액 계산", "예산 초과 확인"],
    non_goals=["날씨 예측", "예약 확정", "결제 실행"],
)


if __name__ == "__main__":
    print("=== Weather Agent Role Card ===")
    print(weather_agent_role.model_dump_json(indent=2))
    print("\n=== Budget Agent Role Card ===")
    print(budget_agent_role.model_dump_json(indent=2))
    print("\n역할이 분리됨:", weather_agent_role.goal != budget_agent_role.goal)
    print("두 Agent 모두 결제 권한이 없음:", "결제 실행" in weather_agent_role.non_goals and "결제 실행" in budget_agent_role.non_goals)
