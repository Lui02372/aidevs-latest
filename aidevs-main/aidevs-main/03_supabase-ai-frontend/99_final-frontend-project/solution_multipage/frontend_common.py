"""99_final-frontend-project 멀티페이지 solution 공통 함수입니다."""

from pathlib import Path
import os

import httpx
import streamlit as st
from dotenv import load_dotenv


# solution_multipage 폴더 기준:
#   C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_multipage
# COURSE_ROOT:
#   C:\aidev\03_supabase-ai-frontend
COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


def init_state() -> None:
    """모든 Streamlit page가 함께 사용할 session_state 기본값을 준비합니다."""

    st.session_state.setdefault("access_token", "")
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("messages", [])


def get_api_base_url() -> str:
    """FastAPI backend 주소를 반환합니다."""

    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def auth_headers() -> dict[str, str]:
    """로그인 후 받은 access_token을 Authorization header로 바꿉니다."""

    token = st.session_state.get("access_token", "")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def request_json(method: str, path: str, **kwargs):
    """backend API를 호출하고, 성공 데이터와 오류 문자열을 반환합니다."""

    url = f"{get_api_base_url()}{path}"

    try:
        response = httpx.request(method, url, timeout=5.0, **kwargs)
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPStatusError as exc:
        return None, f"HTTP {exc.response.status_code}: {exc.response.text}"
    except httpx.RequestError as exc:
        return None, f"백엔드 연결 실패: {exc}"


def signup(email: str, password: str, display_name: str) -> None:
    """회원가입 API를 호출합니다."""

    data, error = request_json(
        "POST",
        "/auth/signup",
        json={
            "email": email,
            "password": password,
            "display_name": display_name,
        },
    )
    if error:
        st.error(error)
    else:
        st.success(f"{data['display_name']}님 회원가입이 완료되었습니다.")


def signin(email: str, password: str) -> None:
    """로그인 API를 호출하고 token과 사용자 정보를 session_state에 저장합니다."""

    data, error = request_json(
        "POST",
        "/auth/signin",
        json={
            "email": email,
            "password": password,
        },
    )
    if error:
        st.error(error)
        return

    st.session_state["access_token"] = data["access_token"]
    st.session_state["current_user"] = data["user"]
    st.success(f"{data['user']['display_name']}님 로그인되었습니다.")


def signout() -> None:
    """로그아웃 API를 호출하고 frontend session_state를 비웁니다."""

    if st.session_state.get("access_token"):
        request_json("POST", "/auth/signout", headers=auth_headers())

    st.session_state["access_token"] = ""
    st.session_state["current_user"] = None
    st.session_state["messages"] = []
    st.success("로그아웃되었습니다.")


def require_login() -> bool:
    """보호 API를 호출하기 전에 로그인 여부를 확인합니다."""

    if not st.session_state.get("access_token"):
        st.warning("먼저 로그인하세요.")
        return False
    return True


def render_connection_status() -> None:
    """사이드바에서 backend 연결 상태를 확인합니다."""

    st.subheader("연결 설정")
    st.code(f"API_BASE_URL={get_api_base_url()}")

    if st.button("백엔드 상태 확인"):
        data, error = request_json("GET", "/health")
        if error:
            st.error(error)
        else:
            st.success("backend 연결 성공")
            st.json(data)


def render_auth_forms() -> None:
    """사이드바에 회원가입/로그인/로그아웃 UI를 표시합니다."""

    st.divider()
    st.subheader("회원가입")
    with st.form("signup_form"):
        signup_email = st.text_input("회원가입 이메일", value="student@example.com")
        signup_name = st.text_input("표시 이름", value="수강생")
        signup_password = st.text_input("회원가입 비밀번호", value="pass1234", type="password")
        signup_submit = st.form_submit_button("회원가입")

    if signup_submit:
        if not signup_email or not signup_name or not signup_password:
            st.warning("회원가입 정보를 모두 입력하세요.")
        else:
            signup(signup_email, signup_password, signup_name)

    st.divider()
    st.subheader("로그인")
    with st.form("signin_form"):
        signin_email = st.text_input("로그인 이메일", value="student@example.com")
        signin_password = st.text_input("로그인 비밀번호", value="pass1234", type="password")
        signin_submit = st.form_submit_button("로그인")

    st.caption("이 예제는 st.session_state 기반 로그인입니다. 브라우저를 새로고침하면 로그인 상태가 초기화될 수 있습니다.")

    if signin_submit:
        if not signin_email or not signin_password:
            st.warning("로그인 정보를 입력하세요.")
        else:
            signin(signin_email, signin_password)

    if st.session_state.get("current_user"):
        st.success(f"현재 사용자: {st.session_state['current_user']['display_name']}")
        st.caption(f"access_token: {st.session_state['access_token']}")
        if st.button("로그아웃"):
            signout()
    else:
        st.info("로그인 전입니다.")


def render_sidebar() -> None:
    """모든 page에서 동일하게 사용하는 sidebar입니다."""

    init_state()
    render_connection_status()
    render_auth_forms()
