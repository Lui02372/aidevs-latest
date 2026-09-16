from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def api(method: str, path: str, payload: dict | None = None) -> dict:
    response = httpx.request(method, f"{BACKEND_URL}{path}", json=payload, timeout=100)
    response.raise_for_status()
    return response.json()


def show_error(error: Exception) -> None:
    if isinstance(error, httpx.HTTPStatusError):
        try:
            detail = error.response.json().get("detail", error.response.text)
        except ValueError:
            detail = error.response.text
        st.error(f"Backend 응답 오류: {detail}")
    else:
        st.error(f"Backend 연결 실패: {error}")
    st.info("Container 상태, Provider 환경 변수와 Backend 로그를 확인하세요.")


st.set_page_config(page_title="Multi-LLM Runtime", page_icon="🐳", layout="wide")
st.title("🐳 Multi-LLM 여행 준비 Chat2")
st.caption("Frontend → Backend → 실제 OpenAI·Gemini·Ollama → Redis·PostgreSQL")

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{uuid4().hex[:8]}"

with st.sidebar:
    provider = st.selectbox("실제 LLM Provider", ["openai", "gemini", "ollama"])
    ollama_model = "gemma"
    if provider == "ollama":
        ollama_model = st.selectbox("Ollama Model", ["gemma", "llama"])
        st.caption(f"Ollama에서 {ollama_model} 모델을 사용합니다.")
    st.code(BACKEND_URL)
    st.code(st.session_state.session_id)
    if st.button("새 대화 시작"):
        try:
            api("DELETE", f"/api/sessions/{st.session_state.session_id}")
            st.session_state.session_id = f"session-{uuid4().hex[:8]}"
            st.rerun()
        except Exception as error:
            show_error(error)

chat_tab, note_tab, status_tab = st.tabs(["Multi-LLM Chat", "여행 메모", "서비스 상태"])

with chat_tab:
    try:
        history = api("GET", f"/api/chat/{st.session_state.session_id}")
        for item in history["messages"]:
            with st.chat_message(item["role"]): st.write(item["content"])
    except Exception as error:
        show_error(error)
    prompt = st.chat_input("여행 준비에 관해 질문하세요.")
    if prompt:
        try:
            result = api("POST", "/api/chat", {
                "session_id": st.session_state.session_id,
                "message": prompt,
                "provider": provider,
                "ollama_model": ollama_model,
            })
            with st.chat_message("assistant"):
                st.write(result["answer"])
                st.caption(f"Provider: {result['provider']} · Model: {result['model']} · Fallback: {result['fallback_used']}")
        except Exception as error:
            show_error(error)

with note_tab:
    with st.form("note-form", clear_on_submit=True):
        name = st.text_input("이름", "홍길동")
        message = st.text_input("여행 메모", "대중교통 이용, 해산물 알레르기")
        submitted = st.form_submit_button("메모 저장", type="primary")
    if submitted:
        try: st.json(api("POST", "/api/notes", {"name": name, "message": message}))
        except Exception as error: show_error(error)
    if st.button("메모 조회"):
        try: st.dataframe(api("GET", "/api/notes")["notes"], use_container_width=True)
        except Exception as error: show_error(error)

with status_tab:
    if st.button("Health 확인"):
        try: st.json(api("GET", "/health"))
        except Exception as error: show_error(error)
    st.info("Provider 실패는 Mock 성공으로 바꾸지 않습니다. 설정되지 않은 Provider는 503을 반환합니다.")
