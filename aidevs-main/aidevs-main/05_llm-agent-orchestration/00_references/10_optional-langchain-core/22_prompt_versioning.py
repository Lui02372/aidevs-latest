"""Prompt를 이름·버전·변경 이유와 함께 코드에서 관리합니다."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate


@dataclass(frozen=True)
class PromptSpec:
    name: str
    version: str
    change_note: str
    template: ChatPromptTemplate


PROMPTS = {
    "v1": PromptSpec(
        name="travel-request-classifier",
        version="1.0.0",
        change_note="최초 분류 기준",
        template=ChatPromptTemplate.from_messages(
            [("system", "여행 요청을 정보 또는 예약으로 분류하세요."), ("human", "{request}")]
        ),
    ),
    "v2": PromptSpec(
        name="travel-request-classifier",
        version="1.1.0",
        change_note="취소 분류와 추측 금지 규칙 추가",
        template=ChatPromptTemplate.from_messages(
            [("system", "여행 요청을 정보, 예약, 취소로 분류하세요. 불명확하면 확인 필요라고 답하세요."),
             ("human", "{request}")]
        ),
    ),
}


if __name__ == "__main__":
    for key, spec in PROMPTS.items():
        print(f"\n{key}: {spec.version} · {spec.change_note}")
        print(spec.template.invoke({"request": "다음 주 예약을 없애고 싶어요"}).to_string())
