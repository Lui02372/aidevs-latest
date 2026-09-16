"""Prompt의 출력 지시와 Pydantic의 애플리케이션 계약을 구분합니다."""

from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class RequestAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intent: Literal["information", "reservation", "unknown"]
    destination: str | None
    confidence: float = Field(ge=0, le=1)
    missing_fields: list[str] = Field(default_factory=list)


prompt = ChatPromptTemplate.from_messages(
    [("system", "요청을 RequestAnalysis schema로 분석하세요. 추측하지 마세요."),
     ("human", "{request}")]
)

samples = [
    {"intent": "information", "destination": "부산", "confidence": 0.9, "missing_fields": []},
    {"intent": "book_now", "destination": "부산", "confidence": 1.4, "missing_fields": [], "extra": True},
]


if __name__ == "__main__":
    print(prompt.invoke({"request": "부산 여행 정보를 알려줘"}).to_string())
    for sample in samples:
        try:
            print("검증 성공:", RequestAnalysis.model_validate(sample).model_dump())
        except ValidationError as error:
            print("검증 실패:", [(item["loc"], item["msg"]) for item in error.errors()])
