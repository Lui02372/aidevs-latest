"""데이터베이스조회 탭입니다."""

import streamlit as st

from frontend_common import sample_database


def render_database_view_tab() -> None:
    """mock 테이블을 선택하고 데이터를 확인합니다."""

    st.subheader("데이터베이스조회")
    st.caption("mock 테이블을 선택하고 데이터를 확인합니다.")

    table_name = st.selectbox("테이블 선택", ["users", "conversations", "service_logs"])
    data = sample_database(table_name)

    st.dataframe(data, use_container_width=True)
    st.caption("실제 Supabase 조회는 backend API를 통해 연결하는 방식으로 확장합니다.")
