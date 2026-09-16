import httpx
import pandas as pd
import streamlit as st


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# 별도의 도시 검색 API를 호출하지 않도록 위도와 경도를 미리 저장합니다.
CITIES = {
    "서울": {"latitude": 37.5665, "longitude": 126.9780},
    "부산": {"latitude": 35.1796, "longitude": 129.0756},
    "대전": {"latitude": 36.3504, "longitude": 127.3845},
    "제주": {"latitude": 33.4996, "longitude": 126.5312},
}


st.title("시간별 날씨 데이터")

city = st.selectbox("도시를 선택하세요", list(CITIES.keys()))
forecast_days = st.slider(
    "조회할 날짜 수",
    min_value=1,
    max_value=7,
    value=2,
)

if st.button("날씨 데이터 조회"):
    location = CITIES[city]

    try:
        with st.spinner("날씨 데이터를 가져오는 중입니다..."):
            response = httpx.get(
                WEATHER_URL,
                params={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "hourly": (
                        "temperature_2m,"
                        "relative_humidity_2m,"
                        "precipitation_probability"
                    ),
                    "forecast_days": forecast_days,
                    "timezone": "Asia/Seoul",
                },
                timeout=10.0,
            )
            response.raise_for_status()
            hourly_data = response.json()["hourly"]

        # 같은 길이의 JSON 배열들을 DataFrame의 각 컬럼으로 변환합니다.
        weather_df = pd.DataFrame(hourly_data)
        # weather_df["time"] = pd.to_datetime(weather_df["time"])

        # # 화면에서 이해하기 쉬운 한글 컬럼명으로 변경합니다.
        weather_df = weather_df.rename(
            columns={
                "time": "시간",
                "temperature_2m": "기온",
                "relative_humidity_2m": "습도",
                "precipitation_probability": "강수확률",
            }
        )

        st.success(f"{city} 날씨 데이터를 가져왔습니다.")

        st.subheader("날씨 데이터 표")
        st.dataframe(
            weather_df,
            use_container_width=True,
            hide_index=True,
        )

        st.write("데이터 개수:", len(weather_df))
        st.write("컬럼 목록:", list(weather_df.columns))

        st.subheader("시간별 기온")
        chart_df = weather_df.set_index("시간")[["기온","습도"]]
        st.line_chart(chart_df)

    except httpx.TimeoutException:
        st.error("날씨 API 응답 시간이 초과되었습니다.")

    except httpx.HTTPStatusError as error:
        st.error(f"날씨 API 오류: {error.response.status_code}")

    except httpx.RequestError:
        st.error("날씨 API 서버에 연결할 수 없습니다.")

    except (KeyError, TypeError, ValueError):
        st.error("API 응답을 DataFrame으로 변환할 수 없습니다.")
