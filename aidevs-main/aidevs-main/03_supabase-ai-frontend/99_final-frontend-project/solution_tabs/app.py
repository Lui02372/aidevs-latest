import os
from pathlib import Path

import httpx
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


COURSE_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(COURSE_ROOT / ".env")


def init_state() -> None:
    st.session_state.setdefault("access_token", "")
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("messages", [])


def get_api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def auth_headers() -> dict[str, str]:
    token = st.session_state.get("access_token", "")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def request_json(method: str, path: str, **kwargs):
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
    if st.session_state.get("access_token"):
        request_json("POST", "/auth/signout", headers=auth_headers())

    st.session_state["access_token"] = ""
    st.session_state["current_user"] = None
    st.session_state["messages"] = []
    st.success("로그아웃되었습니다.")


def require_login() -> bool:
    if not st.session_state.get("access_token"):
        st.warning("먼저 로그인하세요.")
        return False
    return True


init_state()

st.set_page_config(page_title="Personal AI Chatbot", page_icon="AI")
st.title("개인화 AI 챗봇 서비스")
st.caption("backend_mock 또는 backend_service와 연결해 회원가입, 로그인, 챗봇, 대화 기록, 서비스 로그를 확인합니다.")

with st.sidebar:
    st.subheader("연결 설정")
    st.code(f"API_BASE_URL={get_api_base_url()}")

    if st.button("백엔드 상태 확인"):
        data, error = request_json("GET", "/health")
        if error:
            st.error(error)
        else:
            st.success("backend 연결 성공")
            st.json(data)

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
        if st.button("로그아웃"):
            signout()
    else:
        st.info("로그인 전입니다.")

chat_tab, history_tab, log_tab, deploy_tab = st.tabs(
    ["챗봇", "대화 기록", "서비스 로그", "배포 전 점검"]
)

with chat_tab:
    st.subheader("챗봇")

    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input("질문을 입력하세요.", placeholder="예: 오늘 학습한 내용을 요약해줘.")
        chat_submit = st.form_submit_button("전송")

    if chat_submit:
        user_message = user_message.strip()
        if not user_message:
            st.warning("질문을 입력하세요.")
        elif require_login():
            st.session_state["messages"].append({"role": "user", "content": user_message})

            with st.spinner("AI 응답을 생성하는 중입니다..."):
                data, error = request_json(
                    "POST",
                    "/chat",
                    headers=auth_headers(),
                    json={"message": user_message},
                )

            if error:
                st.error(error)
            else:
                answer = data["answer"]
                st.session_state["messages"].append({"role": "assistant", "content": answer})
                st.caption(
                    f"provider={data['provider']}, model={data['model']}, "
                    f"actual_api_called={data['actual_api_called']}"
                )

    st.divider()
    st.caption("대화 내용")

    if not st.session_state["messages"]:
        st.info("아직 대화가 없습니다. 위 입력창에 질문을 입력해 보세요.")
    else:
        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])

with history_tab:
    st.subheader("대화 기록")
    if st.button("대화 기록 새로고침"):
        if require_login():
            data, error = request_json("GET", "/conversations", headers=auth_headers())
            if error:
                st.error(error)
            elif not data:
                st.info("대화 기록이 없습니다.")
            else:
                st.dataframe(pd.DataFrame(data), use_container_width=True)

with log_tab:
    st.subheader("서비스 로그")
    if st.button("서비스 로그 새로고침"):
        if require_login():
            data, error = request_json("GET", "/service-logs", headers=auth_headers())
            if error:
                st.error(error)
            elif not data:
                st.info("서비스 로그가 없습니다.")
            else:
                st.dataframe(pd.DataFrame(data), use_container_width=True)

with deploy_tab:
    st.subheader("배포 전 점검")
    st.checkbox("로컬 프론트 개발은 backend_mock으로 먼저 확인했다.")
    st.checkbox("실제 배포는 backend_service를 Render에 배포해 연결한다.")
    st.checkbox("Render start command는 uvicorn app.main:app --host 0.0.0.0 --port $PORT로 설정한다.")
    st.checkbox("Upstash Redis는 선택 확장이며 token은 backend_service 환경변수에만 둔다.")
    st.checkbox("Streamlit Community Cloud secrets에 API_BASE_URL을 등록한다.")
    st.checkbox("프론트엔드에 service role key, LLM API key, Redis token을 두지 않았다.")
