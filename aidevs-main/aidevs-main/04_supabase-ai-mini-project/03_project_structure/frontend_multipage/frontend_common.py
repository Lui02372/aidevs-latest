"""frontend_multipage 화면들이 함께 사용하는 공통 함수입니다."""

from pathlib import Path
import os

import httpx
import streamlit as st
from dotenv import load_dotenv


# 이 파일 위치:
#   03_project_structure/frontend_multipage/frontend_common.py
# 과정 루트:
#   04_supabase-ai-mini-project
COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


def api_base_url() -> str:
    """FastAPI backend 주소를 반환합니다."""

    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def request_json(method: str, path: str, **kwargs):
    """backend에 JSON 요청을 보내고 결과 또는 오류 메시지를 반환합니다."""

    try:
        response = httpx.request(method, f"{api_base_url()}{path}", timeout=5.0, **kwargs)
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPError as exc:
        return None, str(exc)


def render_backend_status() -> None:
    """사이드바에서 backend 연결 상태를 확인하는 공통 UI입니다."""

    st.subheader("연결")
    st.code(f"API_BASE_URL={api_base_url()}")

    if st.button("backend 상태 확인"):
        data, error = request_json("GET", "/health")
        if error:
            st.error(error)
        else:
            st.success("backend 연결 성공")
            st.json(data)
