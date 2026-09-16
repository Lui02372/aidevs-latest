# [학습] 타입 힌트 평가를 미룬다. 이 파일은 JavaScript가 아니라 Streamlit 서버에서 실행되는 Python이다.
from __future__ import annotations

# [학습] os는 Backend 주소 설정을, uuid4는 새 대화의 임의 식별자 생성을 담당한다.
import os
from uuid import uuid4

# [학습] httpx는 서버 사이 HTTP 통신, st라는 별칭의 streamlit은 화면과 사용자 입력을 담당한다.
import httpx
import streamlit as st


# [학습] BACKEND_URL을 프로세스 환경에서 읽는다. Compose에서는 backend 서비스 이름을 사용하는 주소가 전달된다.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# [학습] 공통 API 함수는 HTTP 메서드·상대 경로·선택 JSON 본문을 받아 JSON 응답을 dict로 돌려준다.
def api(method: str, path: str, payload: dict | None = None) -> dict:
    # [학습] 요청은 브라우저가 아닌 Streamlit 프로세스에서 동기 실행한다. 응답 대기 중 다음 Python 줄로 진행하지 않는다.
    response = httpx.request(method, f"{BACKEND_URL}{path}", json=payload, timeout=100)
    # [학습] 오류 HTTP 응답은 예외로 바꾼다. 각 화면 블록의 except가 show_error로 연결한다.
    response.raise_for_status()
    return response.json()


# [학습] HTTP 오류와 네트워크 등 기타 오류를 구분하여 화면 메시지를 만든다.
def show_error(error: Exception) -> None:
    if isinstance(error, httpx.HTTPStatusError):
        try:
            # [학습] 오류 본문이 JSON이면 detail을 우선 사용하고 해당 키가 없으면 원문 텍스트를 쓴다.
            detail = error.response.json().get("detail", error.response.text)
        # [학습] JSON이 아닌 오류 응답도 있을 수 있어 디코딩 실패 시 텍스트로 처리한다.
        except ValueError:
            detail = error.response.text
        st.error(f"Backend 응답 오류: {detail}")
    else:
        st.error(f"Backend 연결 실패: {error}")
    # [학습] st.error는 오류를, st.info는 사용자가 확인할 위치를 화면에 표시한다.
    st.info("Container 상태, Provider 환경 변수와 Backend 로그를 확인하세요.")


# [학습] 페이지 설정·제목·설명은 스크립트가 실행될 때 화면 요소로 등록된다.
st.set_page_config(page_title="Multi-LLM Runtime", page_icon="🐳", layout="wide")
st.title("🐳 Multi-LLM 여행 준비 Chat2 0914")
st.caption("Frontend → Backend → 실제 OpenAI·Gemini·Ollama → Redis·PostgreSQL")

# [학습] Streamlit은 입력 이벤트에 따라 스크립트를 재실행한다. session_state는 같은 화면 세션의 ID를 유지한다.
if "session_id" not in st.session_state:
    # [학습] UUID의 16진 문자열 앞 8자를 사용한다. 이 ID는 로그인 사용자나 권한을 증명하지 않는다.
    st.session_state.session_id = f"session-{uuid4().hex[:8]}"

# [학습] with st.sidebar 안에서 만든 위젯은 사이드바에 배치된다. with는 여기서 화면 배치 범위를 뜻한다.
with st.sidebar:
    # [학습] selectbox 반환값이 선택 상태다. Ollama일 때만 두 번째 모델 선택 위젯을 만든다.
    provider = st.selectbox("실제 LLM Provider", ["openai", "gemini", "ollama"])
    ollama_model = "gemma"
    if provider == "ollama":
        ollama_model = st.selectbox("Ollama Model", ["gemma", "llama"])
        st.caption(f"Ollama에서 {ollama_model} 모델을 사용합니다.")
    # [학습] 현재 연결 주소와 세션 식별자를 보여 주어 어떤 대화에 요청하는지 확인하게 한다.
    st.code(BACKEND_URL)
    st.code(st.session_state.session_id)
    # [학습] 버튼을 누른 실행에서만 삭제 요청을 보낸다. 성공 후 새 ID로 바꾸고 st.rerun으로 처음부터 다시 그린다.
    if st.button("새 대화 시작"):
        try:
            api("DELETE", f"/api/sessions/{st.session_state.session_id}")
            st.session_state.session_id = f"session-{uuid4().hex[:8]}"
            st.rerun()
        # [학습] 삭제 실패 시 ID 교체와 rerun에 도달하지 않고 오류 화면으로 이어진다.
        except Exception as error:
            show_error(error)

# [학습] 세 탭의 컨테이너를 튜플 언패킹한다. 이 코드의 기본 tabs 사용은 탭 본문을 선택한 탭만 지연 실행하지 않는다.
chat_tab, note_tab, status_tab = st.tabs(["Multi-LLM Chat", "여행 메모", "서비스 상태"])

# [학습] 대화 탭은 매 실행 시 DB 이력 API를 읽는다. 탭을 바꾸는 것과 명시적 API 버튼 조건은 구분한다.
with chat_tab:
    try:
        history = api("GET", f"/api/chat/{st.session_state.session_id}")
        # [학습] 반복문으로 각 기록을 역할별 말풍선 안에 렌더링한다. 한 줄 with도 같은 블록 문법이다.
        for item in history["messages"]:
            with st.chat_message(item["role"]): st.write(item["content"])
    except Exception as error:
        show_error(error)
    # [학습] 입력 제출 시 prompt에 문자열이 생긴다. 값이 없으면 POST를 보내지 않는다.
    prompt = st.chat_input("여행 준비에 관해 질문하세요.")
    if prompt:
        try:
            # [학습] Backend의 ChatRequest와 같은 네 필드로 JSON을 만든다. 모델은 화면에서 직접 호출하지 않는다.
            result = api("POST", "/api/chat", {
                "session_id": st.session_state.session_id,
                "message": prompt,
                "provider": provider,
                "ollama_model": ollama_model,
            })
            # [학습] 요청이 돌아온 뒤 답변과 실제 공급자·모델 정보를 표시한다. 별도 spinner나 토큰 스트리밍 코드는 없다.
            with st.chat_message("assistant"):
                st.write(result["answer"])
                st.caption(f"Provider: {result['provider']} · Model: {result['model']} · Fallback: {result['fallback_used']}")
        # [학습] 실패는 성공 말풍선으로 바꾸지 않고 공통 오류 화면으로 표시한다.
        except Exception as error:
            show_error(error)

# [학습] 메모 입력은 form으로 묶어 제출 시 처리한다. clear_on_submit은 제출 후 폼 입력값을 초기화한다.
with note_tab:
    with st.form("note-form", clear_on_submit=True):
        # [학습] 두 입력 위젯의 반환 문자열을 아래 POST JSON에 넣는다. 기존 예시 입력값은 그대로 유지한다.
        name = st.text_input("이름", "홍길동")
        message = st.text_input("여행 메모", "대중교통 이용, 해산물 알레르기")
        submitted = st.form_submit_button("메모 저장", type="primary")
    # [학습] 제출 이벤트가 참인 실행에서만 저장한다. 반환 JSON에는 Redis 경고가 포함될 수도 있다.
    if submitted:
        try: st.json(api("POST", "/api/notes", {"name": name, "message": message}))
        except Exception as error: show_error(error)
    # [학습] 조회 버튼은 별도 GET을 보내고 notes 목록을 표로 렌더링한다.
    if st.button("메모 조회"):
        try: st.dataframe(api("GET", "/api/notes")["notes"], use_container_width=True)
        except Exception as error: show_error(error)

# [학습] 상태 탭은 버튼을 눌렀을 때만 /health 결과를 표시한다. 주기적인 폴링 코드가 아니다.
with status_tab:
    if st.button("Health 확인"):
        try: st.json(api("GET", "/health"))
        except Exception as error: show_error(error)
    st.info("Provider 실패는 Mock 성공으로 바꾸지 않습니다. 설정되지 않은 Provider는 503을 반환합니다.")
