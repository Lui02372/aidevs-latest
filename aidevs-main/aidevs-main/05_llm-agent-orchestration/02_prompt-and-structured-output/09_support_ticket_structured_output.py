"""분류·판단형 Structured Output인 SupportTicket을 검증합니다."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Literal은 서비스가 처리할 수 있는 분류값만 통과시킵니다.
    category: Literal["billing", "technical", "account", "other"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(min_length=1, max_length=300)
    # strict=True는 "yes"나 1이 Boolean으로 자동 변환되는 것을 막습니다.
    requires_human: bool = Field(strict=True)
    missing_information: list[str] = Field(default_factory=list, max_length=10)


# 생성형 여행 계획과 달리 분류·판단 결과를 계약으로 표현하는 예제입니다.
SAMPLES: dict[str, dict[str, Any]] = {
    "결제 문의": {
        "category": "billing",
        "priority": "medium",
        "summary": "결제가 두 번 승인되었는지 확인이 필요합니다.",
        "requires_human": True,
        "missing_information": ["주문 번호"],
    },
    "기술 문의": {
        "category": "technical",
        "priority": "high",
        "summary": "로그인 후 모든 요청에서 서버 오류가 발생합니다.",
        "requires_human": True,
        "missing_information": ["오류 발생 시각"],
    },
    "허용하지 않은 분류": {
        "category": "refund",
        "priority": "urgent",
        "summary": "환불 요청",
        "requires_human": "yes",
        "missing_information": [],
    },
}


def validate_support_output(name: str, payload: dict[str, Any]) -> None:
    print(f"\n[{name}]")
    try:
        ticket = SupportTicket.model_validate(payload)
        print(ticket.model_dump_json(indent=2))
    except ValidationError as error:
        for item in error.errors():
            location = ".".join(map(str, item["loc"]))
            print(f"- {location}: {item['msg']}")


if __name__ == "__main__":
    for sample_name, sample_payload in SAMPLES.items():
        validate_support_output(sample_name, sample_payload)
