"""로그조회 탭입니다."""

import streamlit as st

from frontend_common import sample_logs


def render_log_view_tab() -> None:
    """mock 로그를 표와 그래프로 확인합니다."""

    st.subheader("로그조회")
    st.caption("mock 로그를 표와 그래프로 확인합니다.")

    logs = sample_logs()
    level_options = ["all"] + sorted(logs["level"].unique().tolist())
    selected_level = st.selectbox("level 필터", level_options)

    if selected_level != "all":
        logs = logs[logs["level"] == selected_level]

    st.dataframe(logs, use_container_width=True)

    st.subheader("level별 로그 수")
    chart_data = logs["level"].value_counts()
    st.bar_chart(chart_data)
