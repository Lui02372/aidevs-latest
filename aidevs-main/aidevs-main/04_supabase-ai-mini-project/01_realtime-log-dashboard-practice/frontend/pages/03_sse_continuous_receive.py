r"""3. SSE 3분 자동 수신 화면입니다.

이 화면은 02_sse_timed_receive.py와 같은 방식으로 SSE를 수신합니다.
차이점은 사용자가 시작 버튼을 누르지 않아도, 화면에 들어오면 자동으로 수신을 시작한다는 점입니다.

실행:
    streamlit run .\app.py
    왼쪽 메뉴에서 "3. SSE 3분 자동 수신"을 선택합니다.
"""

import time

import httpx
import pandas as pd
import streamlit as st

from frontend_common import api_base_url, parse_sse_data, render_backend_status


AUTO_RECEIVE_SECONDS = 180


st.title("3. SSE 3분 자동 수신")
st.caption(
    "화면이 열리면 자동으로 `GET /stream/logs` 연결을 열고, 약 3분 동안 새 로그 이벤트를 수신합니다."
)

st.info(
    "이 화면은 2번 화면과 같은 Python SSE 수신 방식을 사용합니다. "
    "2번은 사용자가 버튼을 눌러 수신을 시작하고, 3번은 화면 진입 시 자동으로 수신을 시작합니다. "
    "수신된 이벤트는 최근 이벤트 표와 level별 그래프로 함께 확인합니다."
)

with st.sidebar:
    st.subheader("연결")
    st.code(f"API_BASE_URL={api_base_url()}")
    render_backend_status()

st.markdown(
    """
    확인 순서:

    1. 이 화면을 열면 자동으로 SSE 수신이 시작됩니다.
    2. 다른 브라우저 탭에서 `http://127.0.0.1:8000/docs`를 엽니다.
    3. Swagger에서 `POST /logs`를 여러 번 실행합니다.
    4. 아래 표와 그래프에 새 로그 이벤트가 표시되는지 확인합니다.

    이 화면은 수업용으로 약 3분 동안만 자동 수신합니다.
    다시 수신하려면 왼쪽 메뉴에서 다른 화면을 눌렀다가 다시 이 화면으로 돌아오거나,
    브라우저에서 새로고침합니다.
    """
)

st.code(f"{api_base_url()}/stream/logs")

summary_box = st.empty()
chart_box = st.empty()
stream_box = st.empty()
status_box = st.empty()

summary_box.info("자동 수신을 준비하고 있습니다.")
chart_box.caption("수신된 log 이벤트의 `level` 값을 기준으로 그래프가 표시됩니다.")

events: list[dict] = []
log_events: list[dict] = []
started = time.time()

try:
    status_box.info(f"SSE 자동 수신 중입니다. 최대 {AUTO_RECEIVE_SECONDS}초 동안 실행됩니다.")

    with httpx.stream("GET", f"{api_base_url()}/stream/logs", timeout=None) as response:
        response.raise_for_status()

        for line in response.iter_lines():
            item = parse_sse_data(line)
            if item:
                # heartbeat는 backend가 연결 유지를 위해 보내는 신호입니다.
                # 실제 로그가 아니므로 표와 그래프 집계에서는 제외합니다.
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

            if time.time() - started > AUTO_RECEIVE_SECONDS:
                break

    status_box.success("3분 자동 수신이 종료되었습니다. 다시 확인하려면 화면을 새로고침하세요.")
except httpx.HTTPError as exc:
    status_box.error(f"SSE 연결 실패: {exc}")

if not log_events:
    st.warning(
        "자동 수신 시간 동안 새 log 이벤트가 없었습니다. "
        "다른 탭에서 POST /logs를 실행한 뒤 이 화면을 다시 열어 보세요."
    )
