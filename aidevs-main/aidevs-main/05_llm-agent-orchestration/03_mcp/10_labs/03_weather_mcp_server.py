"""현재 날씨와 단기 예보를 제공하는 교육용 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "weather",
    instructions="부산과 서울의 현재 날씨와 단기 예보를 제공합니다.",
)


@mcp.tool()
def get_current_weather(city: Literal["부산", "서울"]) -> dict:
    """도시의 현재 날씨를 조회합니다."""
    weather = {
        "부산": {"condition": "맑음", "temperature_c": 24},
        "서울": {"condition": "흐림", "temperature_c": 21},
    }
    return {
        "city": city,
        **weather[city],
        "source": "lab-weather-service",
    }


@mcp.tool()
def get_weather_forecast(
    city: Literal["부산", "서울"],
    days: int = 1,
) -> dict:
    """오늘을 제외한 향후 며칠의 날씨 예보를 조회합니다."""
    if not 1 <= days <= 3:
        raise ValueError("days는 1에서 3 사이여야 합니다.")

    forecasts = {
        "부산": [
            {"day": "내일", "condition": "오후 한때 비", "min_c": 19, "max_c": 25},
            {"day": "모레", "condition": "맑음", "min_c": 18, "max_c": 26},
            {"day": "3일 후", "condition": "구름 많음", "min_c": 20, "max_c": 27},
        ],
        "서울": [
            {"day": "내일", "condition": "흐림", "min_c": 16, "max_c": 23},
            {"day": "모레", "condition": "비", "min_c": 15, "max_c": 20},
            {"day": "3일 후", "condition": "맑음", "min_c": 14, "max_c": 22},
        ],
    }
    return {
        "city": city,
        "forecast": forecasts[city][:days],
        "source": "lab-weather-forecast-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
