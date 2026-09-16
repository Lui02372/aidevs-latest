r"""최근 대화 이력을 백엔드로 함께 보내는 챗봇 클라이언트 실습입니다.

실행 전 준비:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    cd .\05_ai-chatbot-interface\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

프론트엔드 실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\05_ai-chatbot-interface\10_labs\lab-04-context-chat-client.py

이 실습은 기본적으로 /api/chat/mock을 호출합니다.
Gemini 실제 호출은 04_mock-and-optional-gemini-interface의 06~08 예제를 참고합니다.
"""

import httpx  # FastAPI 백엔드 API에 HTTP 요청을 보내기 위해 사용합니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


API_BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = "/api/chat/mock"

# 최근 6개 메시지, 즉 최근 3턴 정도만 백엔드로 보냅니다.
# 전체 대화를 계속 보내면 요청 데이터가 커지고 LLM 비용도 늘어날 수 있습니다.
# 나중에는 서비스 정책에 따라 더 많은 메시지를 보내거나,
# 오래된 대화를 요약해서 보내거나,
# DB/Vector DB에서 필요한 기억만 검색해 함께 보내는 방식으로 확장할 수 있습니다.
HISTORY_LIMIT = 6


def reset_messages():
    """화면에 저장된 대화 이력을 초기화합니다."""

    st.session_state["lab_context_messages"] = []


def make_recent_history(messages):
    """백엔드로 전송할 최근 대화 이력 payload를 만듭니다."""

    history = []

    for message in messages[-HISTORY_LIMIT:]:
        history.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    return history


def call_chat_api(question, history):
    """현재 질문과 최근 대화 이력을 백엔드 chat API로 보냅니다."""

    payload = {
        "question": question,
        "messages": history,
    }
    response = httpx.post(f"{API_BASE_URL}{CHAT_ENDPOINT}", json=payload, timeout=5.0)
    response.raise_for_status()
    return response.json()


st.title("최근 대화 이력 전송 실습")
st.caption("최근 6개 메시지를 함께 보내 백엔드가 문맥을 참고할 수 있는 구조를 연습합니다.")
st.code(f"POST {API_BASE_URL}{CHAT_ENDPOINT}", language="text")

if "lab_context_messages" not in st.session_state:
    st.session_state["lab_context_messages"] = []

with st.sidebar:
    st.subheader("대화 상태")
    st.write(f"저장된 메시지 수: {len(st.session_state['lab_context_messages'])}")
    st.write(f"백엔드로 보낼 최근 메시지 수: 최대 {HISTORY_LIMIT}개")
    st.button("대화 초기화", on_click=reset_messages)

for message in st.session_state["lab_context_messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if "history_sent" in message:
            st.caption(f"백엔드로 함께 보낸 이전 메시지 수: {message['history_sent']}개")

prompt = st.chat_input("이전 대화를 이어서 질문해 보세요")

if prompt:
    recent_history = make_recent_history(st.session_state["lab_context_messages"])

    st.session_state["lab_context_messages"].append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    try:
        with st.spinner("최근 대화 이력을 함께 보내는 중입니다..."):
            result = call_chat_api(prompt, recent_history)

        st.session_state["lab_context_messages"].append(
            {
                "role": "assistant",
                "content": result["answer"],
                "history_sent": len(recent_history),
            }
        )
    except httpx.ConnectError:
        st.session_state["lab_context_messages"].append(
            {
                "role": "assistant",
                "content": "챗봇 백엔드에 연결할 수 없습니다. 05_ai-chatbot-interface/00_sample_backend를 먼저 실행하세요.",
                "history_sent": len(recent_history),
            }
        )
    except httpx.TimeoutException:
        st.session_state["lab_context_messages"].append(
            {
                "role": "assistant",
                "content": "응답 시간이 초과되었습니다. 잠시 후 다시 시도하세요.",
                "history_sent": len(recent_history),
            }
        )
    except httpx.HTTPStatusError as error:
        st.session_state["lab_context_messages"].append(
            {
                "role": "assistant",
                "content": f"백엔드 API 오류가 발생했습니다. status={error.response.status_code}",
                "history_sent": len(recent_history),
            }
        )

    st.rerun()
