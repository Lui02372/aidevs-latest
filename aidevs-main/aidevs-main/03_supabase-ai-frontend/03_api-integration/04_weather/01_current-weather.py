# 01_current-weather.py

import httpx
import streamlit as st


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# 도시 검색 API를 추가로 호출하지 않도록 도시별 좌표를 미리 저장합니다.
CITIES = {
    "서울": {"latitude": 37.5665, "longitude": 126.9780},
    "부산": {"latitude": 35.1796, "longitude": 129.0756},
    "대전": {"latitude": 36.3504, "longitude": 127.3845},
    "제주": {"latitude": 33.4996, "longitude": 126.5312},
}


st.title("현재 날씨 조회")

city = st.selectbox("도시를 선택하세요", list(CITIES.keys()))

if st.button("날씨 조회"):
    location = CITIES[city]

    try:
        with st.spinner("날씨 정보를 가져오는 중입니다..."):
            response = httpx.get(
                WEATHER_URL,
                params={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "current": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "apparent_temperature,"
                        "weather_code,"
                        "wind_speed_10m"
                    ),
                    "timezone": "Asia/Seoul",
                },
                timeout=10.0,
            )
            response.raise_for_status()
            weather = response.json()["current"]

        st.success("날씨 정보를 가져왔습니다.")
        st.subheader(f"{city} 현재 날씨")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("기온", f"{weather['temperature_2m']} °C")

        with col2:
            st.metric(
                "체감온도",
                f"{weather['apparent_temperature']} °C",
            )

        with col3:
            st.metric(
                "습도",
                f"{weather['relative_humidity_2m']} %",
            )

        st.write("풍속:", weather["wind_speed_10m"], "km/h")
        st.write("날씨 코드:", weather["weather_code"])

        with st.expander("API 원본 응답"):
            st.json(response.json())

    except httpx.TimeoutException:
        st.error("날씨 API 응답 시간이 초과되었습니다.")

    except httpx.HTTPStatusError as error:
        st.error(f"날씨 API 오류: {error.response.status_code}")

    except httpx.RequestError:
        st.error("날씨 서버에 연결할 수 없습니다.")

    except (KeyError, TypeError, ValueError):
        st.error("날씨 응답 형식이 예상과 다릅니다.")
