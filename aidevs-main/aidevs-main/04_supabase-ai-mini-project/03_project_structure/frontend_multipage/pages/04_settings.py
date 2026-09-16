r"""설정 확인 화면입니다."""

import streamlit as st

from frontend_common import api_base_url, render_backend_status


st.title("설정")
st.caption("로컬 실행과 배포 후 연결 정보를 확인하는 화면입니다.")

with st.sidebar:
    render_backend_status()

st.subheader("현재 연결 정보")
st.code(f"API_BASE_URL={api_base_url()}")

st.markdown(
    """
    최종 프로젝트에서 이 화면에 정리하면 좋은 정보:

    - 로컬 backend 주소
    - Render에 배포한 backend 주소
    - Streamlit Community Cloud 배포 주소
    - Supabase 프로젝트 URL
    - Upstash Redis 사용 여부
    """
)
