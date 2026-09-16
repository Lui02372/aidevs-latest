"""06_streamlit-multipage-app에서 함께 사용하는 공통 코드입니다."""

from datetime import datetime

import pandas as pd
import streamlit as st


def init_state() -> None:
    """모든 page에서 사용할 session_state 기본값을 준비합니다."""

    st.session_state.setdefault("is_logged_in", False)
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("registered_users", [])


def login(email: str, display_name: str) -> None:
    """mock 로그인입니다. 실제 인증 API 호출 없이 session_state만 바꿉니다."""

    st.session_state["is_logged_in"] = True
    st.session_state["current_user"] = {
        "email": email,
        "display_name": display_name,
        "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def logout() -> None:
    """mock 로그아웃입니다."""

    st.session_state["is_logged_in"] = False
    st.session_state["current_user"] = None
    st.session_state["chat_messages"] = []


def render_login_sidebar() -> None:
    """왼쪽 sidebar에 공통 로그인 UI를 표시합니다."""

    init_state()

    st.subheader("로그인")

    if st.session_state["is_logged_in"]:
        user = st.session_state["current_user"]
        st.success(f"{user['display_name']}님 로그인 중")
        st.caption(user["email"])
        st.caption(f"로그인 시간: {user['login_time']}")
        if st.button("로그아웃"):
            logout()
            st.rerun()
        return

    with st.form("sidebar_login_form"):
        email = st.text_input("이메일", value="student@example.com")
        display_name = st.text_input("이름", value="수강생")
        submitted = st.form_submit_button("로그인")

    if submitted:
        if not email or not display_name:
            st.warning("이메일과 이름을 입력하세요.")
        else:
            login(email, display_name)
            st.rerun()


def require_login() -> bool:
    """로그인이 필요한 화면에서 로그인 상태를 확인합니다."""

    init_state()
    if not st.session_state["is_logged_in"]:
        st.warning("왼쪽 sidebar에서 먼저 로그인하세요.")
        return False
    return True


def sample_logs() -> pd.DataFrame:
    """로그조회 화면에서 사용할 mock 로그 데이터입니다."""

    return pd.DataFrame(
        [
            {
                "time": "09:10:12",
                "level": "info",
                "screen": "Chat",
                "message": "사용자 질문 입력",
                "latency_ms": 80,
            },
            {
                "time": "09:10:15",
                "level": "info",
                "screen": "Chat",
                "message": "mock 답변 생성",
                "latency_ms": 120,
            },
            {
                "time": "09:11:03",
                "level": "warning",
                "screen": "Database",
                "message": "검색 조건 없이 전체 조회",
                "latency_ms": 210,
            },
            {
                "time": "09:12:41",
                "level": "error",
                "screen": "Login",
                "message": "비어 있는 이메일 입력",
                "latency_ms": 30,
            },
        ]
    )


def sample_database(table_name: str) -> pd.DataFrame:
    """데이터베이스조회 화면에서 사용할 mock 테이블 데이터입니다."""

    tables = {
        "users": [
            {"id": 1, "email": "student@example.com", "display_name": "수강생"},
            {"id": 2, "email": "coach@example.com", "display_name": "강사"},
        ],
        "conversations": [
            {"id": 101, "user_id": 1, "message": "오늘 학습 내용 요약해줘", "role": "user"},
            {"id": 102, "user_id": 1, "message": "Streamlit pages 구조를 정리해드릴게요.", "role": "assistant"},
        ],
        "service_logs": [
            {"id": 1001, "level": "info", "message": "chat request received"},
            {"id": 1002, "level": "info", "message": "mock answer generated"},
        ],
    }
    return pd.DataFrame(tables[table_name])
