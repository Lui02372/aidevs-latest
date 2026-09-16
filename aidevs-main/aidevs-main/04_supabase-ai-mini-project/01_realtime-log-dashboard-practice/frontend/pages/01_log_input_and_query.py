r"""1. 로그 입력/조회 화면입니다.

이 화면에서는 REST API 흐름을 확인합니다.

실행:
    streamlit run .\app.py
    왼쪽 사이드바에서 "01 log input and query" 화면을 선택합니다.
"""

import pandas as pd
import streamlit as st

from frontend_common import api_base_url, render_backend_status, request_json


st.title("1. 로그 입력/조회")
st.caption(
    "REST API로 로그를 생성하고, Supabase DB 또는 memory fallback에 저장된 최근 로그를 다시 조회합니다."
)

st.info(
    "`POST /logs`는 로그를 저장합니다. `GET /logs`는 이미 저장된 로그 목록을 다시 조회합니다. "
    "응답의 `storage_mode`가 `supabase`이면 DB 저장, `memory`이면 교육용 임시 저장입니다."
)

with st.sidebar:
    st.subheader("연결")
    st.code(f"API_BASE_URL={api_base_url()}")
    render_backend_status()

left, right = st.columns([1, 2])

with left:
    st.subheader("로그 생성")
    st.caption("`POST /logs`를 호출해 새 서비스 로그를 만듭니다.")

    level = st.selectbox("level", ["info", "warning", "error"])
    source = st.text_input("source", value="chat-api")
    message = st.text_area("message", value="AI 응답 생성 완료")
    latency_ms = st.number_input("latency_ms", min_value=0, value=120)
    status_code = st.number_input("status_code", min_value=100, value=200)

    if st.button("POST /logs", type="primary"):
        payload = {
            "level": level,
            "source": source,
            "message": message,
            "request_path": "/chat",
            "status_code": int(status_code),
            "latency_ms": int(latency_ms),
            "metadata": {"course": "04-mini-project"},
        }
        data, error = request_json("POST", "/logs", json=payload)
        if error:
            st.error(error)
        else:
            st.success("로그를 생성했습니다.")
            st.json(data)
            st.caption("`storage_mode`로 Supabase DB 저장인지 memory fallback 저장인지 확인합니다.")

with right:
    st.subheader("최근 로그 조회")
    st.caption("`GET /logs`로 저장된 최근 로그를 조회합니다.")

    limit = st.slider("조회 개수", min_value=5, max_value=100, value=50, step=5)

    if st.button("GET /logs 새로고침"):
        data, error = request_json("GET", f"/logs?limit={limit}")
        if error:
            st.error(error)
        elif not data:
            st.info("저장된 로그가 없습니다.")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            if "level" in df:
                st.bar_chart(df["level"].value_counts())

    if st.button("GET /logs/summary"):
        data, error = request_json("GET", "/logs/summary")
        if error:
            st.error(error)
        else:
            st.json(data)
