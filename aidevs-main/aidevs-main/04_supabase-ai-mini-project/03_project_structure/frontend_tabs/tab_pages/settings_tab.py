"""설정 확인 탭입니다."""

import streamlit as st

from frontend_common import api_base_url, render_backend_status


def render_settings_tab() -> None:
    """backend 연결 정보와 배포 관련 설정을 확인합니다."""

    st.subheader("설정")
    st.code(f"API_BASE_URL={api_base_url()}")
    render_backend_status()

    st.markdown(
        """
        최종 프로젝트에서 이 탭에 정리하면 좋은 정보:

        - 로컬 backend 주소
        - Render backend 배포 주소
        - Streamlit Community Cloud 배포 주소
        - Supabase 프로젝트 URL
        - Upstash Redis 사용 여부
        """
    )
