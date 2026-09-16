r"""데이터베이스조회 화면입니다."""

import streamlit as st

from frontend_common import render_login_sidebar, require_login, sample_database


st.title("데이터베이스조회")
st.caption("실제 DB 연결 없이 테이블 선택과 조회 화면 구성을 연습합니다.")

with st.sidebar:
    render_login_sidebar()

if require_login():
    table_name = st.selectbox("조회할 테이블", ["users", "conversations", "service_logs"])
    data = sample_database(table_name)

    st.dataframe(data, use_container_width=True)
    st.caption("이 화면은 mock 데이터입니다. 실제 Supabase 조회는 backend API를 통해 연결합니다.")
else:
    st.info("데이터베이스조회 화면은 로그인 후 확인할 수 있습니다.")
