"""화면 설명 탭입니다."""

import streamlit as st


def render_overview_tab() -> None:
    """탭 기반 화면 구조와 06 multipage 구조의 차이를 설명합니다."""

    st.subheader("화면 설명")
    st.info(
        "이 예제는 한 Streamlit 앱 안에서 탭을 눌러 화면을 전환하는 구조입니다. "
        "각 탭의 내용은 tab_pages 폴더의 함수로 분리합니다."
    )

    st.markdown(
        """
        | 탭 | 구현할 내용 |
        | --- | --- |
        | 회원가입 | 입력폼과 결과 메시지 |
        | 로그조회 | 표, 필터, 그래프 |
        | Chat | 메시지 입력과 대화 누적 |
        | 데이터베이스조회 | 테이블 선택과 데이터 표시 |
        """
    )

    st.caption("06은 왼쪽 메뉴 기반, 07은 상단 탭 기반입니다.")
