r"""SSE 실시간 수신 화면입니다.

학생 구현 예:
    - GET /stream/logs 연결
    - 새 로그 이벤트 표시
    - heartbeat는 실제 로그 집계에서 제외
"""

import streamlit as st

from frontend_common import api_base_url, render_backend_status


st.title("실시간 수신")
st.caption("SSE로 새 로그 이벤트를 받는 화면입니다.")

with st.sidebar:
    render_backend_status()

st.code(f"{api_base_url()}/stream/logs")
st.info(
    "여기에 `httpx.stream()`을 사용한 SSE 수신 코드를 구현합니다. "
    "구현 방식은 `01_realtime-log-dashboard-practice/frontend/pages/02_sse_timed_receive.py`를 참고합니다."
)

st.markdown(
    """
    구현 체크리스트:

    - 새 로그 이벤트를 표로 표시
    - level별 그래프 표시
    - heartbeat 이벤트 제외
    - 연결 오류 메시지 표시
    """
)
