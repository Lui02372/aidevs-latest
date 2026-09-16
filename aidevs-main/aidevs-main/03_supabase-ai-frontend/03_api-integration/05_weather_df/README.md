# 05 Weather DataFrame

Open-Meteo API에서 시간별 날씨 데이터를 받아 pandas DataFrame으로 변환하고,
Streamlit 화면에 표와 선 그래프로 표시하는 예제입니다.

## 학습 흐름

```text
외부 날씨 API 호출
-> JSON 응답에서 hourly 데이터 추출
-> pandas DataFrame으로 변환
-> Streamlit 표 출력
-> 시간별 기온 차트 출력
```

## 실행

```powershell
cd C:\aidevs\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\03_api-integration\05_weather_df\01_weather-dataframe.py
```

화면에서 도시와 조회할 날짜 수를 선택한 뒤 `날씨 데이터 조회` 버튼을 누릅니다.

## 주요 컬럼

| 컬럼 | 의미 |
| --- | --- |
| `시간` | 날씨 데이터의 기준 시각 |
| `기온` | 지상 2m 기온(°C) |
| `습도` | 지상 2m 상대습도(%) |
| `강수확률` | 시간별 강수확률(%) |

이 예제는 API 키 없이 Open-Meteo의 Forecast API 하나만 호출합니다.
