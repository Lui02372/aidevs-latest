r"""회원가입, 로그인, 로그인 후 화면 전환을 한 번에 확인하는 Streamlit 예제입니다.

먼저 샘플 백엔드를 실행합니다.

    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    cd .\04_state-session-and-data\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

그 다음 새 PowerShell에서 이 Streamlit 예제를 실행합니다.

    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\03_auth-token-and-login-state\04_signup-login-screen-change.py

이 예제의 핵심:
    - 회원가입은 POST /api/signup을 호출합니다.
    - 로그인은 POST /api/login을 호출합니다.
    - 로그인 성공 시 access_token을 st.session_state에 저장합니다.
    - access_token이 있으면 로그인 후 화면을 보여 줍니다.
    - 로그아웃하면 access_token을 지우고 다시 로그인 전 화면으로 돌아갑니다.
"""

import httpx
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


def initialize_session_state() -> None:
    """화면 재실행 후에도 유지할 값을 처음 한 번만 준비합니다."""

    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "display_name" not in st.session_state:
        st.session_state.display_name = None


def is_logged_in() -> bool:
    """현재 로그인 상태인지 확인합니다."""

    return st.session_state.access_token is not None


def build_auth_headers() -> dict[str, str]:
    """보호된 API 호출에 사용할 Authorization header를 만듭니다."""

    return {"Authorization": f"Bearer {st.session_state.access_token}"}


def show_logged_out_screen() -> None:
    """로그인 전 화면입니다. 회원가입과 로그인을 탭으로 나누어 보여 줍니다."""

    st.info("아직 로그인하지 않았습니다. 회원가입 후 로그인해 보세요.")

    signup_tab, login_tab = st.tabs(["회원가입", "로그인"])

    with signup_tab:
        st.subheader("회원가입")
        signup_username = st.text_input("새 사용자 이름", value="newstudent")
        signup_display_name = st.text_input("표시 이름", value="새 수강생")
        signup_password = st.text_input("새 비밀번호", value="1234", type="password")

        if st.button("회원가입", type="primary"):
            try:
                response = httpx.post(
                    f"{API_BASE_URL}/api/signup",
                    json={
                        "username": signup_username,
                        "password": signup_password,
                        "display_name": signup_display_name,
                    },
                    timeout=5.0,
                )
                if response.status_code == 201:
                    st.success(response.json()["message"])
                    st.caption("이제 로그인 탭에서 방금 만든 계정으로 로그인합니다.")
                else:
                    st.error(response.json().get("detail", "회원가입에 실패했습니다."))
            except httpx.ConnectError:
                st.error("샘플 백엔드에 연결할 수 없습니다. 00_sample_backend를 먼저 실행하세요.")

    with login_tab:
        st.subheader("로그인")
        username = st.text_input("사용자 이름", value="student")
        password = st.text_input("비밀번호", value="1234", type="password")

        if st.button("로그인", type="primary"):
            try:
                response = httpx.post(
                    f"{API_BASE_URL}/api/login",
                    json={"username": username, "password": password},
                    timeout=5.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.access_token = data["access_token"]
                    st.session_state.username = data["username"]
                    st.session_state.display_name = data["display_name"]
                    st.rerun()
                else:
                    st.error(response.json().get("detail", "로그인에 실패했습니다."))
            except httpx.ConnectError:
                st.error("샘플 백엔드에 연결할 수 없습니다. 00_sample_backend를 먼저 실행하세요.")


def show_logged_in_screen() -> None:
    """로그인 후 화면입니다. token이 있을 때만 이 화면이 보입니다."""

    st.success(f"{st.session_state.display_name}님, 로그인 상태입니다.")
    st.write("사용자 이름:", st.session_state.username)
    st.caption("access_token은 화면에 직접 노출하지 않고 session_state에만 보관합니다.")

    if st.button("내 정보 조회"):
        try:
            response = httpx.get(
                f"{API_BASE_URL}/api/me",
                headers=build_auth_headers(),
                timeout=5.0,
            )
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(response.json().get("detail", "사용자 정보를 조회하지 못했습니다."))
        except httpx.ConnectError:
            st.error("샘플 백엔드에 연결할 수 없습니다.")

    if st.button("로그아웃"):
        st.session_state.access_token = None
        st.session_state.username = None
        st.session_state.display_name = None
        st.rerun()


st.title("회원가입과 로그인 상태 전환")
st.caption("04_state-session-and-data/00_sample_backend를 먼저 실행한 뒤 테스트합니다.")

initialize_session_state()

if is_logged_in():
    show_logged_in_screen()
else:
    show_logged_out_screen()
