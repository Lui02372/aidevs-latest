"""Tool을 정의하고 schema 검증과 직접 실행을 확인하는 API Key 없는 예제."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    city: str = Field(min_length=1, description="검색할 도시")
    limit: int = Field(default=3, ge=1, le=5, description="최대 결과 수")


@tool(args_schema=SearchInput)
def search_attractions(city: str, limit: int = 3) -> list[dict[str, str]]:
    """도시의 교육용 Mock 관광지 정보를 검색합니다."""
    items = [
        {"name": f"{city} 해변", "category": "자연"},
        {"name": f"{city} 전통시장", "category": "음식"},
        {"name": f"{city} 박물관", "category": "문화"},
    ]
    return items[:limit]


if __name__ == "__main__":
    print("도구 이름:", search_attractions.name)
    print("도구 설명:", search_attractions.description)
    print("JSON Schema:", search_attractions.args_schema.model_json_schema())
    print("실행 결과:", search_attractions.invoke({"city": "부산", "limit": 2}))
