r"""로그 입력과 조회 화면입니다.

학생 구현 예:
    - POST /logs로 테스트 로그 생성
    - GET /logs로 최근 로그 조회
    - level/status별 그래프 표시
"""

import pandas as pd
import streamlit as st

from frontend_common import render_backend_status, request_json


st.title("로그 대시보드")
st.caption("로그 입력, 조회, 표와 그래프를 구현하는 화면입니다.")

with st.sidebar:
    render_backend_status()

st.subheader("구현할 기능")
st.markdown(
    """
    - 로그 메시지 입력 폼
    - `POST /logs` 호출
    - `GET /logs` 조회
    - 최근 로그 테이블
    - level별 또는 status별 그래프
    """
)

if st.button("샘플 backend health 조회"):
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
