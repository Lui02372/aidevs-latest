r"""서비스 로그 조회 화면입니다."""

import pandas as pd
import streamlit as st

from frontend_common import auth_headers, init_state, render_sidebar, request_json, require_login


init_state()

st.title("3. 서비스 로그")
st.caption("챗봇 사용 과정에서 backend가 남긴 서비스 로그를 조회합니다.")

with st.sidebar:
    render_sidebar()

st.info("이 화면은 보호 API인 `GET /service-logs`를 호출합니다. 로그인 후 받은 token이 Authorization header로 전달됩니다.")

if st.button("서비스 로그 새로고침", type="primary"):
    if require_login():
        data, error = request_json("GET", "/service-logs", headers=auth_headers())
        if error:
            st.error(error)
        elif not data:
            st.info("서비스 로그가 없습니다.")
        else:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
