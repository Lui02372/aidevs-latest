r"""사용자 피드백 분석 화면입니다.

학생 구현 예:
    - AI 답변에 대한 사용자 평가 입력
    - 피드백 목록 조회
    - 만족/불만족 비율 그래프
"""

import streamlit as st

from frontend_common import render_backend_status


st.title("피드백 분석")
st.caption("사용자 피드백 데이터를 바탕으로 AI 답변 품질을 점검하는 화면입니다.")

with st.sidebar:
    render_backend_status()

st.markdown(
    """
    이 화면에 구현할 수 있는 기능:

    - `POST /feedback`으로 사용자 피드백 저장
    - `GET /feedback`으로 피드백 목록 조회
    - 좋은 응답과 나쁜 응답의 비율 시각화
    - 자주 등장하는 개선 요청 정리
    """
)
