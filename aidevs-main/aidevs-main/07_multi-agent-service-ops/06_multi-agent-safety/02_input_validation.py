"""
[시나리오]
Prompt Injection 검사를 통과한 요청을 Input Validation Agent가 구조적으로 검사합니다.

1. 여행지는 비어 있으면 안 됩니다.
2. 여행 일수는 1~14일, 인원은 1~20명이어야 합니다.
3. 사용자 요청은 YAML 정책에 정한 최대 길이를 넘을 수 없습니다.
4. 올바른 입력과 잘못된 입력을 각각 실행해 차이를 확인합니다.

[기대 결과]
- 올바른 입력은 검증된 TravelRequest로 변환됩니다.
- 잘못된 입력은 프로그램을 숨겨서 성공시키지 않고 검증 오류를 출력합니다.

[학습 포인트]
LLM에게 숫자 범위를 판단시키지 않습니다. 형식과 범위는 Pydantic과 Python이
결정적으로 검사하고, LLM에는 검증을 통과한 값만 전달합니다.
"""

from pydantic import BaseModel, Field, ValidationError, field_validator

from security_registry import load_security_policies


class TravelRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=50)
    days: int = Field(ge=1, le=14)
    people: int = Field(ge=1, le=20)
    user_message: str

    @field_validator("destination")
    @classmethod
    def destination_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("여행지는 공백일 수 없습니다.")
        return value.strip()

    @field_validator("user_message")
    @classmethod
    def message_must_fit_policy(cls, value: str) -> str:
        max_length = load_security_policies()["input"]["max_length"]
        if len(value) > max_length:
            raise ValueError(f"사용자 요청은 {max_length}자를 넘을 수 없습니다.")
        return value


def input_validation_agent(raw_request: dict[str, object]) -> None:
    try:
        validated = TravelRequest.model_validate(raw_request)
        print("검증 성공:", validated.model_dump())
    except ValidationError as error:
        print("검증 실패:", error.errors(include_url=False))


input_validation_agent({"destination": "부산", "days": 3, "people": 2, "user_message": "맛집 중심으로 계획해 줘."})
input_validation_agent({"destination": "  ", "days": 30, "people": 0, "user_message": "여행 계획"})
