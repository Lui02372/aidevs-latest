"""Streamlit frontend 화면들이 함께 사용하는 공통 함수입니다."""

from pathlib import Path
import json
import os

import httpx
import streamlit as st
from dotenv import load_dotenv


# frontend 폴더 기준:
#   C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\frontend
# COURSE_ROOT:
#   C:\aidev\04_supabase-ai-mini-project
COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


def api_base_url() -> str:
    """FastAPI backend 주소를 반환합니다."""

    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def request_json(method: str, path: str, **kwargs):
    """FastAPI backend에 JSON 요청을 보내고, 성공 데이터와 오류 문자열을 반환합니다."""

    try:
        response = httpx.request(method, f"{api_base_url()}{path}", timeout=5.0, **kwargs)
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPError as exc:
        return None, str(exc)


def parse_sse_data(line: str) -> dict | None:
    """SSE 응답 한 줄에서 `data:` JSON만 꺼냅니다."""

    if not line.startswith("data: "):
        return None
    return json.loads(line.removeprefix("data: ").strip())


def render_backend_status() -> None:
    """사이드바에서 backend 상태를 확인하는 공통 UI입니다."""

    if st.button("백엔드 상태 확인"):
        data, error = request_json("GET", "/health")
        if error:
            st.error(error)
        else:
            st.json(data)
            st.caption(
                "expected_*는 설정값 기준 예상 모드이고, "
                "last_*는 최근 요청에서 실제로 사용된 모드입니다."
            )
