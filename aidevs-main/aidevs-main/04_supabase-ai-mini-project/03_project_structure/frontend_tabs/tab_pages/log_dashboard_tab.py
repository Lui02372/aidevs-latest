"""로그 대시보드 탭입니다."""

import pandas as pd
import streamlit as st

from frontend_common import request_json


def render_log_dashboard_tab() -> None:
    """로그 입력, 조회, 그래프 영역을 구현하는 탭입니다."""

    st.subheader("로그 대시보드")
    st.caption("여기에 로그 입력, 조회, 표와 그래프를 구현합니다.")

    if st.button("샘플 backend health 조회", key="log_health"):
        data, error = request_json("GET", "/health")
        if error:
            st.error(error)
        else:
            st.json(data)

    sample = pd.DataFrame(
        [
            {"level": "info", "count": 3},
            {"level": "warning", "count": 1},
            {"level": "error", "count": 1},
        ]
    )
    st.bar_chart(sample.set_index("level"))
