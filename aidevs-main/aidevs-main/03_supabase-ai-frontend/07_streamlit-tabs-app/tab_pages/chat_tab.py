"""Chat 탭입니다."""
import httpx
import streamlit as st

from frontend_common import require_login

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

def render_chat_tab() -> None:
    """로그인 후 mock 대화를 입력하고 누적 표시합니다."""

    st.subheader("Chat")
    st.caption("로그인 후 mock 대화를 입력하고 누적 표시합니다.")

    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("메시지 입력", placeholder="오늘 배운 내용을 정리해줘.")
        submitted = st.form_submit_button("전송")

    if submitted:

        if not message:
            st.warning("메시지를 입력하세요.")
        else:
            message = message.strip()
            payload = {"user_id": "id01", "prompt": message}  # 백엔드 Pydantic 모델이 기대하는 JSON 구조로 데이터를 만듭니다.
            with st.spinner("전송후 기다립니다."):
                response = httpx.post(f"{API_BASE_URL}/chat/gemini", json=payload, timeout=15.0)  # 메시지 API에 POST 요청을 보냅니다.
            if response.status_code == 200:
                result = response.json()
                st.info(message)
                st.info(result["answer"])
            else:
                st.warning("오류")
      