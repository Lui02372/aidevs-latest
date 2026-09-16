r"""로그조회 화면입니다."""

import streamlit as st

from frontend_common import render_login_sidebar, require_login, sample_logs


st.title("로그조회")
st.caption("서비스 로그 테이블 화면을 mock 데이터로 구성합니다.")

with st.sidebar:
    render_login_sidebar()

if require_login():
    logs = sample_logs()
    level = st.selectbox("level 필터", ["all", "info", "warning", "error"])

    if level != "all":
        logs = logs[logs["level"] == level]

    st.dataframe(logs, use_container_width=True)
    st.bar_chart(logs["level"].value_counts())
else:
    st.info("로그조회 화면은 로그인 후 확인할 수 있습니다.")
