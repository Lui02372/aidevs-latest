"""호텔 검색과 취소 규정 조회를 제공하는 교육용 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "hotel",
    instructions="도시와 가격 조건으로 호텔을 검색하고 호텔별 취소 규정을 제공합니다.",
)

HOTELS = [
    {
        "hotel_id": "hotel-busan-001",
        "name": "바다 호텔",
        "city": "부산",
        "price": 120_000,
    },
    {
        "hotel_id": "hotel-busan-002",
        "name": "항구 호텔",
        "city": "부산",
        "price": 170_000,
    },
    {
        "hotel_id": "hotel-seoul-001",
        "name": "도시 호텔",
        "city": "서울",
        "price": 140_000,
    },
]

CANCELLATION_POLICIES = {
    "hotel-busan-001": "체크인 3일 전까지 취소하면 전액 환불합니다.",
    "hotel-busan-002": "체크인 7일 전까지 취소하면 전액 환불합니다.",
    "hotel-seoul-001": "체크인 2일 전까지 취소하면 전액 환불합니다.",
}


@mcp.tool()
def search_hotels(
    city: Literal["부산", "서울"],
    max_price: int = 150_000,
) -> dict:
    """도시와 1박 최대 가격으로 호텔을 검색합니다."""
    if max_price < 1:
        raise ValueError("max_price는 1 이상이어야 합니다.")
    matches = [
        hotel for hotel in HOTELS
        if hotel["city"] == city and hotel["price"] <= max_price
    ]
    return {"items": matches, "source": "lab-hotel-catalog"}


@mcp.tool()
def get_cancellation_policy(hotel_id: str) -> dict:
    """호텔 검색 결과의 hotel_id로 해당 호텔의 취소 규정을 조회합니다."""
    policy = CANCELLATION_POLICIES.get(hotel_id)
    if policy is None:
        raise ValueError(f"존재하지 않는 hotel_id입니다: {hotel_id}")
    hotel = next(hotel for hotel in HOTELS if hotel["hotel_id"] == hotel_id)
    return {
        "hotel_id": hotel_id,
        "hotel_name": hotel["name"],
        "policy": policy,
        "source": "lab-hotel-policy-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
