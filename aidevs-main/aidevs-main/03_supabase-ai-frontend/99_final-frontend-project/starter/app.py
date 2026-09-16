import os
from pathlib import Path

import httpx
import streamlit as st
from dotenv import load_dotenv


COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


def get_api_base_url() -> str:
    """프론트엔드가 호출할 백엔드 주소를 환경변수에서 읽습니다."""
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def check_backend_health(api_base_url: str) -> tuple[bool, str]:
    """백엔드 /health API를 호출해 연결 상태를 확인합니다."""
    try:
        response = httpx.get(f"{api_base_url}/health", timeout=3.0)
        if response.status_code == 200:
            return True, response.text
        return False, f"HTTP {response.status_code}: {response.text}"
    except httpx.RequestError as exc:
        return False, f"백엔드 연결 실패: {exc}"


st.set_page_config(page_title="Final Frontend Starter", page_icon="UI")

st.title("Final Frontend Project Starter")
st.caption("Streamlit 화면이 FastAPI 백엔드를 호출하는 최소 예제입니다.")

api_base_url = st.text_input("API_BASE_URL", value=get_api_base_url())

if st.button("백엔드 /health 확인"):
    with st.spinner("백엔드 연결을 확인하는 중입니다..."):
        ok, message = check_backend_health(api_base_url)

    if ok:
        st.success("백엔드 연결 성공")
        st.code(message)
    else:
        st.error(message)

st.divider()

st.subheader("프로젝트 화면 확장 위치")
user_message = st.text_input("사용자 질문 예시", placeholder="질문을 입력하세요.")

if st.button("mock 응답 표시"):
    if not user_message.strip():
        st.warning("질문을 먼저 입력하세요.")
    else:
        st.chat_message("user").write(user_message)
        st.chat_message("assistant").write("여기에 백엔드 응답 또는 mock 응답을 표시합니다.")
