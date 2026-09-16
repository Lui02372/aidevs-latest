"""세 Provider가 같은 TravelPlan Schema를 반환하는지 비교합니다."""

from time import perf_counter

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from provider_factory import create_chat_model


class TravelPlan(BaseModel):
    destination: str
    summary: str
    recommended_days: int = Field(ge=1, le=30)
    activities: list[str] = Field(min_length=1)
    cautions: list[str] = Field(default_factory=list)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "요청을 TravelPlan Schema에 맞는 여행 일정으로 변환하세요."),
        ("human", "{message}"),
    ]
)

for provider_name in ("openai", "gemini", "ollama"):
    try:
        model = create_chat_model(provider_name).with_structured_output(TravelPlan)
        started = perf_counter()
        result = (prompt | model).invoke(
            {"message": "부산 대중교통 2박 3일 여행을 제안해 주세요."}
        )
        print(f"\n[{provider_name}] {round((perf_counter() - started) * 1000)}ms")
        print(result.model_dump_json(indent=2))
    except Exception as error:
        print(f"\n[{provider_name}] 실행 실패: {error}")
