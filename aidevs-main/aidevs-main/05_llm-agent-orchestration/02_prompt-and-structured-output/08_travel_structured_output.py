"""LLM이 만들었다고 가정한 TravelPlan JSON을 검증합니다."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class TravelPlan(BaseModel):
    # LLM이 임의 필드를 추가해도 계약을 통과하지 못하게 합니다.
    model_config = ConfigDict(extra="forbid")

    destination: str = Field(min_length=1)
    summary: str = Field(min_length=1, max_length=500)
    recommended_days: int = Field(ge=1, le=30)
    activities: list[str] = Field(min_length=1, max_length=10)
    cautions: list[str] = Field(default_factory=list, max_length=10)


# 성공, 누락, 범위 오류, 추가 필드라는 대표 경계 조건을 한 번씩 확인합니다.
SAMPLES: dict[str, dict[str, Any]] = {
    "정상 여행 계획": {
        "destination": "부산",
        "summary": "대중교통으로 대표 명소를 둘러보는 일정",
        "recommended_days": 3,
        "activities": ["해운대 산책", "전통시장 방문"],
        "cautions": ["방문 전 운영 시간을 확인하세요."],
    },
    "필수 필드 누락": {
        "destination": "제주",
        "summary": "자연 명소 중심 일정",
        "recommended_days": 2,
        "cautions": [],
    },
    "범위를 벗어난 값": {
        "destination": "강릉",
        "summary": "여행",
        "recommended_days": 0,
        "activities": [],
        "cautions": [],
    },
    "계약에 없는 필드": {
        "destination": "서울",
        "summary": "도심 명소 일정",
        "recommended_days": 2,
        "activities": ["박물관 방문"],
        "cautions": [],
        "password": "Schema 밖의 값",
    },
}


def validate_travel_output(name: str, payload: dict[str, Any]) -> None:
    print(f"\n[{name}]")
    try:
        # JSON 파싱 이후에도 필드 타입과 범위를 별도로 검증해야 합니다.
        plan = TravelPlan.model_validate(payload)
        print(plan.model_dump_json(indent=2))
    except ValidationError as error:
        for item in error.errors():
            location = ".".join(map(str, item["loc"]))
            print(f"- {location}: {item['msg']}")


if __name__ == "__main__":
    for sample_name, sample_payload in SAMPLES.items():
        validate_travel_output(sample_name, sample_payload)
