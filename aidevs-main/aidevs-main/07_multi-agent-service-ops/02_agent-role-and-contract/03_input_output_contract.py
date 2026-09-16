"""Lab 02-03: 자유 문자열 대신 명시적인 Agent 입출력 계약을 만듭니다.

시나리오:
    Budget Agent가 "부산 여행 예산을 짜 줘"라는 문장만 받으면 기간과 예산 한도를
    추측해야 합니다. 입력 계약으로 필수 정보를 정하고 출력 계약으로 다음 Agent가
    읽을 필드를 고정합니다.

학습 질문:
    자연어 Prompt만으로 Agent 사이의 데이터 형식을 보장할 수 있을까요?

확인할 내용:
    입력과 출력이 Pydantic Model로 검증되고 다음 단계가 필드 이름을 예측하지 않아도
    됩니다. 이 단계는 계약 구조 예제이므로 실제 LLM을 호출하지 않습니다.
"""

from typing import Literal

from pydantic import BaseModel, Field


class BudgetAgentInput(BaseModel):
    destination: str
    days: int = Field(ge=1, le=30)
    total_budget: int = Field(gt=0)


class BudgetAgentOutput(BaseModel):
    agent_id: Literal["budget_agent"] = "budget_agent"
    summary: str
    completed: bool


def budget_agent(request: BudgetAgentInput) -> BudgetAgentOutput:
    return BudgetAgentOutput(
        summary=f"{request.destination} {request.days}일 여행을 {request.total_budget:,}원 안에서 계획합니다.",
        completed=True,
    )


if __name__ == "__main__":
    agent_input = BudgetAgentInput(destination="부산", days=3, total_budget=600_000)
    agent_output = budget_agent(agent_input)
    print("입력 계약:")
    print(agent_input.model_dump_json(indent=2))
    print("\n출력 계약:")
    print(agent_output.model_dump_json(indent=2))
    print("\n완료 여부를 문자열 Parsing 없이 확인:", agent_output.completed)
