r"""전체 화면 구조를 설명하는 첫 화면입니다."""

import streamlit as st

from frontend_common import render_backend_status


st.title("AI 서비스 로그 대시보드")
st.caption("왼쪽 메뉴 기반 multipage 구조입니다.")

st.info(
    "이 화면은 최종 프로젝트의 전체 메뉴 구성을 보여 주는 자리입니다. "
    "팀 프로젝트에서는 기능별 담당자가 각 page 파일을 맡아 구현할 수 있습니다."
)

st.markdown(
    """
    | 메뉴 | 구현할 내용 |
    | --- | --- |
    | 로그 대시보드 | 로그 생성, 로그 조회, 표와 그래프 |
    | 실시간 수신 | SSE로 새 로그 이벤트 표시 |
    | 피드백 분석 | 사용자 피드백 조회와 AI 답변 품질 개선 지표 |
    | 설정 | backend 주소, 배포 URL, 환경 설정 확인 |
    """
)

with st.sidebar:
    render_backend_status()
