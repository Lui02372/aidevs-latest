"""
[MCP 배포 시나리오]
Weather Agent의 실제 날씨 Tool을 분리된 MCP Server로 실행합니다. Container에서는
0.0.0.0:8010으로 공개하며 오류를 고정 Mock 날씨로 성공 처리하지 않습니다.
"""

from __future__ import annotations

import os

import httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "Travel Real Data Tools",
    instructions="Open-Meteo의 실제 도시 좌표와 날씨 예보를 제공합니다.",
    host=os.getenv("MCP_HOST", "127.0.0.1"),
    port=int(os.getenv("MCP_PORT", "8010")),
    json_response=True,
)


async def geocode(city: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ko", "format": "json"},
        )
        response.raise_for_status()
    results = response.json().get("results") or []
    if not results:
        raise ValueError(f"도시를 찾을 수 없습니다: {city}")
    item = results[0]
    return {
        "name": item["name"],
        "country": item.get("country"),
        "latitude": item["latitude"],
        "longitude": item["longitude"],
        "timezone": item.get("timezone"),
    }


@mcp.tool()
async def resolve_destination(city: str) -> dict[str, object]:
    """Open-Meteo Geocoding API에서 실제 도시 좌표를 조회합니다."""
    return await geocode(city)


@mcp.tool()
async def get_weather(city: str, forecast_days: int = 3) -> dict[str, object]:
    """Open-Meteo Forecast API에서 최대 7일의 실제 일별 날씨 예보를 조회합니다."""
    if not 1 <= forecast_days <= 7:
        raise ValueError("forecast_days는 1~7이어야 합니다.")
    location = await geocode(city)
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "auto",
                "forecast_days": forecast_days,
            },
        )
        response.raise_for_status()
    daily = response.json().get("daily")
    if not daily:
        raise RuntimeError("Open-Meteo가 일별 예보를 반환하지 않았습니다.")
    return {"source": "Open-Meteo", "location": location, "daily": daily}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
