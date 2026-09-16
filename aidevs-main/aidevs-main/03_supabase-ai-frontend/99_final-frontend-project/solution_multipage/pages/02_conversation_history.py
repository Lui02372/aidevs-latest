r"""대화 기록 조회 화면입니다."""

import pandas as pd
import streamlit as st

from frontend_common import auth_headers, init_state, render_sidebar, request_json, require_login


init_state()

st.title("2. 대화 기록")
st.caption("로그인한 사용자의 이전 대화 기록을 backend에서 조회합니다.")

with st.sidebar:
    render_sidebar()

st.info("이 화면은 보호 API인 `GET /conversations`를 호출합니다. 로그인 후 받은 token이 Authorization header로 전달됩니다.")

if st.button("대화 기록 새로고침", type="primary"):
    if require_login():
        data, error = request_json("GET", "/conversations", headers=auth_headers())
        if error:
            st.error(error)
        elif not data:
            st.info("대화 기록이 없습니다.")
        else:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
