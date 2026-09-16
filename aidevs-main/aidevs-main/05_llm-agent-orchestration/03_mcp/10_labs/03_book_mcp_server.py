"""특정 지역 호텔 예약 처리하는 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "book",
    instructions="특정 지역 호텔 예약 처리를 수행합니다.",
)


@mcp.tool()
def book_hotels(
    hotel_id: Literal["hotel-busan-001", "hotel-busan-002", "hotel-seoul-001", "hotel-seoul-002"],
    date: str,
    nights: int,
    guests: int,
) -> dict:
    """호텔 예약을 처리합니다."""
    print(f"{hotel_id} {date} {nights}")
    return {"status": "ok"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
