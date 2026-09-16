"""사용자 피드백 분석 탭입니다."""

import streamlit as st


def render_feedback_analysis_tab() -> None:
    """AI 답변 품질 개선을 위한 피드백 분석 영역입니다."""

    st.subheader("피드백 분석")
    st.markdown(
        """
        이 탭에 구현할 수 있는 기능:

        - 사용자 피드백 입력
        - 피드백 목록 조회
        - 만족/불만족 비율 그래프
        - 개선이 필요한 답변 유형 정리
        """
    )
