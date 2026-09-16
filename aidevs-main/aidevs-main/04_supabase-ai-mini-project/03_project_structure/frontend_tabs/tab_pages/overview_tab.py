"""화면 설명 탭입니다."""

import streamlit as st


def render_overview_tab() -> None:
    """탭 기반 화면 구조와 구현 범위를 설명합니다."""

    st.subheader("화면 설명")
    st.info(
        "이 구조는 한 Streamlit 화면 안에서 탭을 눌러 내용을 전환합니다. "
        "탭별 코드는 tab_pages 폴더의 파일로 분리합니다."
    )

    st.markdown(
        """
        | 탭 | 구현할 내용 |
        | --- | --- |
        | 로그 대시보드 | 로그 생성, 로그 조회, 표와 그래프 |
        | 실시간 수신 | SSE로 새 로그 이벤트 표시 |
        | 피드백 분석 | 사용자 피드백 조회와 AI 답변 품질 개선 지표 |
        | 설정 | backend 주소, 배포 URL, 환경 설정 확인 |
        """
    )
