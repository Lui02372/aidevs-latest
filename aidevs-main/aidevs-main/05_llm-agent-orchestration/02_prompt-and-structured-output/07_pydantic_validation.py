"""일반 dict를 Pydantic 모델로 검증하는 최소 예제입니다."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ReservationRequest(BaseModel):
    # 계약에 없는 값이 조용히 버려지지 않도록 추가 필드를 거부합니다.
    model_config = ConfigDict(extra="forbid")

    customer_name: str = Field(min_length=1)
    reservation_date: date
    people: int = Field(ge=1, le=20)
    children: int = Field(default=0, ge=0, le=10)


def validate_sample(name: str, payload: dict) -> None:
    print(f"\n[{name}]")
    try:
        request = ReservationRequest.model_validate(payload)
        print("검증 성공:", request.model_dump(mode="json"))
    except ValidationError as error:
        # errors()는 화면이나 API 오류 형식으로 변환하기 쉬운 구조화 목록입니다.
        print("검증 실패:")
        for item in error.errors():
            location = ".".join(map(str, item["loc"]))
            print(f"- {location}: {item['msg']}")


if __name__ == "__main__":
    validate_sample(
        "정상 데이터",
        {
            "customer_name": "김여행",
            "reservation_date": "2026-08-10",
            "people": 2,
            "children": 1,  # 계약에 없는 필드이므로 무시됩니다.
        },
    )
    validate_sample(
        "잘못된 값",
        {
            "customer_name": "",
            "reservation_date": "잘못된 날짜",
            "people": 0,
        },
    )
    validate_sample(
        "계약에 없는 필드",
        {
            "customer_name": "김여행",
            "reservation_date": "2026-08-10",
            "people": 2,
            "password": "abc123",
        },
    )
