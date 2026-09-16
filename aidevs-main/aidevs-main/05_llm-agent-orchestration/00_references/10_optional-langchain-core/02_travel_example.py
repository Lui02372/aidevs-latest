"""여행 요청을 일정 초안으로 바꾸는 Mock LangChain 예제."""

from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableLambda


class DayPlan(BaseModel):
    day: int
    activities: list[str]


class TravelPlan(BaseModel):
    destination: str
    days: list[DayPlan]
    estimated_budget: int = Field(gt=0)
    warnings: list[str] = Field(default_factory=list)


def extract_request(data: dict) -> dict:
    return {
        "destination": data.get("destination", "부산"),
        "nights": int(data.get("nights", 2)),
        "budget": int(data.get("budget", 500000)),
    }


def mock_plan(data: dict) -> TravelPlan:
    day_count = data["nights"] + 1
    days = [
        DayPlan(day=day, activities=[f"{data['destination']} 추천 장소 {day}", "지역 음식 체험"])
        for day in range(1, day_count + 1)
    ]
    return TravelPlan(
        destination=data["destination"],
        days=days,
        estimated_budget=min(data["budget"], day_count * 120000),
        warnings=["가격은 교육용 Mock 데이터입니다."],
    )


chain = RunnableLambda(extract_request) | RunnableLambda(mock_plan)


if __name__ == "__main__":
    result = chain.invoke({"destination": "부산", "nights": 2, "budget": 500000})
    print(result.model_dump_json(indent=2))
