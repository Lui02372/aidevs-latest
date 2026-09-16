"""SSE 실시간 수신 탭입니다."""

import streamlit as st

from frontend_common import api_base_url


def render_realtime_stream_tab() -> None:
    """SSE 실시간 이벤트 수신 영역을 구현하는 탭입니다."""

    st.subheader("실시간 수신")
    st.code(f"{api_base_url()}/stream/logs")
    st.info(
        "여기에 `httpx.stream()`을 사용한 SSE 수신 코드를 구현합니다. "
        "구현 방식은 `01_realtime-log-dashboard-practice/frontend/pages/02_sse_timed_receive.py`를 참고합니다."
    )
