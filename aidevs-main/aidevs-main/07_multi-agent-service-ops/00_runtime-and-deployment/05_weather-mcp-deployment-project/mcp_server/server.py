"""
시나리오
사용자가 선택한 도시의 실제 날씨를 Open-Meteo에서 조회하는 MCP Tool Server입니다.
Backend만 Docker 내부 주소 weather-mcp:8010으로 접근하며 Host에는 8010을 공개하지 않습니다.
도시를 좌표로 변환한 뒤 오늘 또는 내일의 최고·최저 기온과 강수 확률을 반환합니다.
"""

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Open-Meteo 지오코딩은 한글 질의를 일부만 인식하고(서울·제주 등은 결과가 없음) 국가 필터가
# 없으면 동명 외국 도시를 먼저 반환한다(제주→에티오피아, 안양→중국). 아래 표기는 한글 질의가
# 실패할 때만 쓰는 대체 검색어이며 김해는 매큔-라이샤워 표기만 색인되어 있다.
KOREAN_CITY_ROMANIZATION = {
    "서울": "Seoul", "용인": "Yongin", "평택": "Pyeongtaek", "시흥": "Siheung",
    "김포": "Gimpo", "김해": "Kimhae", "청주": "Cheongju", "천안": "Cheonan",
    "전주": "Jeonju", "군산": "Gunsan", "익산": "Iksan", "경주": "Gyeongju",
    "춘천": "Chuncheon", "강릉": "Gangneung", "제주": "Jeju", "서귀포": "Seogwipo",
}
ADMIN_SUFFIXES = ("특별자치시", "특별자치도", "특별시", "광역시", "시", "도", "군")

mcp = FastMCP("weather-tools", host="0.0.0.0", port=8010, stateless_http=True, json_response=True)

def is_korean(text: str) -> bool:
    """한글 음절이 하나라도 있으면 한국 지명 질의로 본다."""
    return any("가" <= character <= "힣" for character in text)

def normalize_korean_city(city: str) -> str:
    """'경기도 수원시'처럼 입력해도 마지막 낱말의 행정구역 접미사를 떼어 '수원'으로 맞춘다."""
    name = city.split()[-1] if city.split() else city
    for suffix in ADMIN_SUFFIXES:
        if name.endswith(suffix) and len(name) > len(suffix) + 1:
            return name[: -len(suffix)]
    return name

def search_place(client: httpx.Client, name: str, country_code: str | None = None) -> dict | None:
    params = {"name": name, "count": 1, "language": "ko", "format": "json"}
    if country_code:
        params["countryCode"] = country_code
    response = client.get(GEOCODING_URL, params=params)
    response.raise_for_status()
    places = response.json().get("results", [])
    return places[0] if places else None

def resolve_place(client: httpx.Client, city: str) -> dict | None:
    """한글 입력은 대한민국으로 한정해 조회하고 실패하면 로마자 표기로 한 번 더 시도한다."""
    if not is_korean(city):
        return search_place(client, city)
    name = normalize_korean_city(city)
    return (
        search_place(client, name, "KR")
        or search_place(client, KOREAN_CITY_ROMANIZATION.get(name, name), "KR")
        or search_place(client, city)
    )

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True))
def get_weather(city: str, day: str = "tomorrow") -> dict:
    """도시 이름과 today 또는 tomorrow를 받아 실제 일별 날씨를 반환합니다."""
    if day not in {"today", "tomorrow"}:
        raise ValueError("day는 today 또는 tomorrow여야 합니다.")
    with httpx.Client(timeout=15) as client:
        place = resolve_place(client, city)
        if place is None:
            return {"success": False, "error": "CITY_NOT_FOUND", "city": city}
        forecast = client.get("https://api.open-meteo.com/v1/forecast", params={"latitude": place["latitude"], "longitude": place["longitude"], "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code", "timezone": "auto", "forecast_days": 2})
        forecast.raise_for_status()
    daily = forecast.json()["daily"]
    index = 0 if day == "today" else 1
    return {"success": True, "city": place["name"], "country": place.get("country"), "date": daily["time"][index], "temperature_max": daily["temperature_2m_max"][index], "temperature_min": daily["temperature_2m_min"][index], "precipitation_probability": daily["precipitation_probability_max"][index], "weather_code": daily["weather_code"][index], "source": "Open-Meteo"}

@mcp.custom_route("/health", methods=["GET"])
async def health(_request):
    return JSONResponse({"status": "ok", "service": "weather-mcp"})

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
