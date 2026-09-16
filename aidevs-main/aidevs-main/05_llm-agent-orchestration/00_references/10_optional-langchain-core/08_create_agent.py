"""LangChain 1.x create_agent로 Model→Tool→Model 반복을 실행합니다.

실행 전 LANGCHAIN_PROVIDER(openai/gemini/ollama)와 해당 Provider 환경 변수를
설정합니다. Tool 결과는 교육용 Mock 데이터이며 실제 예약을 수행하지 않습니다.
"""

import os

from langchain.agents import create_agent
from langchain_core.tools import tool

from provider_factory import create_chat_model


@tool
def get_weather(city: str) -> str:
    """도시의 교육용 Mock 날씨를 조회합니다."""
    return f"{city}: 맑음, 23도 (Mock 데이터)"


@tool
def search_attractions(city: str) -> list[str]:
    """도시의 교육용 Mock 관광지를 검색합니다."""
    return [f"{city} 해변", f"{city} 전통시장"]


provider = os.getenv("LANGCHAIN_PROVIDER", "openai")
agent = create_agent(
    model=create_chat_model(provider),
    tools=[get_weather, search_attractions],
    system_prompt="여행 도우미입니다. 필요한 경우 도구를 사용하고 Mock임을 밝히세요.",
)


if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "부산 날씨와 관광지 두 곳을 알려줘."}]}
    )
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")
