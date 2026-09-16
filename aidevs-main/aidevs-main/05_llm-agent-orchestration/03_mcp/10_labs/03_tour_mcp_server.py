"""특정 지역의 관광지 정보를 조회하는 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "tour",
    instructions="도시에 관광지를 검색하고 관광지별 정보를 제공합니다.",
)

TOURISTS = [
    {
        "tourist_id": "tourist-busan-001",
        "name": "바다 관광지",
        "city": "부산",
    },
    {
        "tourist_id": "tourist-busan-002",
        "name": "항구 관광지",
        "city": "부산",
    },
    {
        "tourist_id": "tourist-seoul-001",
        "name": "도시 관광지",
        "city": "서울",
    },
    {
        "tourist_id": "tourist-seoul-002",
        "name": "한강 관광지",
        "city": "서울",
    },
]


@mcp.tool()
def search_tourists(
    city: Literal["부산", "서울"],
) -> dict:
    """도시에 관광지를 검색합니다."""
    matches = [
        tourist for tourist in TOURISTS
        if tourist["city"] == city          
    ]
    return {"items": matches, "source": "lab-tourist-catalog"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
