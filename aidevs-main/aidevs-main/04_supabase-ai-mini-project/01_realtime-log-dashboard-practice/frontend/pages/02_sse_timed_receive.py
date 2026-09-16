r"""2. SSE 시간 설정 수신 화면입니다.

이 화면에서는 정해진 시간 동안만 SSE 연결을 열어 새 로그 이벤트를 받습니다.

실행:
    streamlit run .\app.py
    왼쪽 사이드바에서 "02 sse timed receive" 화면을 선택합니다.
"""

import time

import httpx
import pandas as pd
import streamlit as st

from frontend_common import api_base_url, parse_sse_data, render_backend_status


st.title("2. SSE 시간 설정 수신")
st.caption("정해진 시간 동안 `GET /stream/logs` 연결을 열고, 그 시간 안에 새로 발생한 로그 이벤트만 받습니다.")

st.info(
    "이 화면은 저장된 전체 로그를 조회하지 않습니다. "
    "버튼을 누른 이후 새로 발생한 이벤트만 Redis pub/sub 또는 memory queue를 통해 받습니다."
)

with st.sidebar:
    st.subheader("연결")
    st.code(f"API_BASE_URL={api_base_url()}")
    render_backend_status()

st.markdown(
    """
    확인 순서:

    1. 이 화면에서 `GET /stream/logs 실시간 보기`를 누릅니다.
    2. 다른 브라우저 탭에서 `http://127.0.0.1:8000/docs`를 엽니다.
    3. Swagger에서 `POST /logs`를 실행합니다.
    4. 아래 표에 `event: log` 데이터가 들어오는지 확인합니다.
    """
)

seconds = st.slider("수신 시간(초)", min_value=5, max_value=60, value=15)
summary_box = st.empty()
chart_box = st.empty()
stream_box = st.empty()

summary_box.info("아직 수신을 시작하지 않았습니다. 버튼을 누른 뒤 다른 화면에서 새 로그를 생성해 보세요.")
chart_box.caption("수신된 log 이벤트의 `level` 값을 기준으로 그래프가 표시됩니다.")

if st.button("GET /stream/logs 실시간 보기", type="primary"):
    events: list[dict] = []
    log_events: list[dict] = []
    started = time.time()

    try:
        with httpx.stream("GET", f"{api_base_url()}/stream/logs", timeout=None) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                item = parse_sse_data(line)
                if item:
                    # heartbeat는 연결 유지용 신호이므로 화면 표와 그래프에서는 제외합니다.
                    if item.get("message") == "SSE 연결 유지 중입니다.":
                        continue

                    events.insert(0, item)
                    if "level" in item:
                        log_events.insert(0, item)

                    summary_box.info(f"현재까지 {len(log_events)}개의 log 이벤트를 수신했습니다.")
                    stream_box.dataframe(pd.DataFrame(events[:20]), use_container_width=True)

                    if log_events:
                        chart_data = pd.DataFrame(log_events)["level"].value_counts()
                        chart_box.bar_chart(chart_data)

                if time.time() - started > seconds:
                    break
    except httpx.HTTPError as exc:
        st.error(f"SSE 연결 실패: {exc}")

    if not log_events:
        st.warning("수신 시간 동안 새 이벤트가 없었습니다. 다른 탭에서 POST /logs를 실행해 보세요.")
