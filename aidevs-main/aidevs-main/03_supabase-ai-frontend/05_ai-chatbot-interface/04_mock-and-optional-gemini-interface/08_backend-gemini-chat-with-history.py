r"""최근 대화 이력을 백엔드로 함께 보내 문맥을 이어가는 Streamlit 예제입니다.

실행 전 준비:
    1. 05_ai-chatbot-interface/00_sample_backend/.env에 GEMINI_API_KEY를 설정합니다.
    2. 05_ai-chatbot-interface/00_sample_backend를 먼저 실행합니다.

백엔드 실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    cd .\05_ai-chatbot-interface\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

프론트엔드 실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\08_backend-gemini-chat-with-history.py

주의:
    이 예제는 질문을 보낼 때 최근 대화 이력 일부를 함께 백엔드로 전송합니다.
    본격적인 사용자별 대화 저장, 요약 memory, DB 기반 memory는 04_state-session-and-data와 이후 과정에서 다룹니다.
"""

import os  # API_BASE_URL을 환경변수에서 읽기 위해 사용합니다.

import httpx  # FastAPI 백엔드 API에 HTTP 요청을 보내기 위해 사용합니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
CHAT_ENDPOINT = "/api/chat/gemini"

# 지금은 최근 6개 메시지만 백엔드로 보냅니다.
# 6개 메시지는 보통 user/assistant 3턴 정도의 대화입니다.
# 전체 대화를 계속 보내면 요청 데이터가 커지고 LLM 비용도 늘어날 수 있습니다.
# 나중에는 서비스 정책에 따라 더 많은 메시지를 보내거나,
# 오래된 대화를 요약해서 보내거나,
# DB/Vector DB에서 필요한 기억만 검색해 함께 보내는 방식으로 확장할 수 있습니다.
HISTORY_LIMIT = 6


def reset_messages():
    """현재 화면에 저장된 대화 이력을 모두 삭제합니다."""

    st.session_state["context_messages"] = []


def to_backend_history(messages):
    """화면에 저장된 메시지 중 백엔드로 보낼 최근 대화 이력만 추립니다."""

    # 오류 메시지나 메타데이터는 백엔드로 보내지 않고, role/content만 보냅니다.
    # Gemini가 문맥으로 참고할 수 있는 최소 정보만 보내는 것이 이 예제의 기준입니다.
    history = []

    for message in messages[-HISTORY_LIMIT:]:
        if message["role"] in ("user", "assistant"):
            history.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                }
            )

    return history


def call_gemini_chat_api(message, history):
    """질문과 최근 대화 이력을 함께 백엔드 Gemini chat API로 보냅니다."""

    # 백엔드는 question만 받아도 동작하지만,
    # 여기서는 messages를 함께 보내 Gemini가 최근 문맥을 참고하도록 합니다.
    payload = {
        "question": message,
        "messages": history,
    }
    response = httpx.post(f"{API_BASE_URL}{CHAT_ENDPOINT}", json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()


st.title("백엔드 Gemini 문맥 대화 예제")
st.caption("최근 대화 6개 메시지를 백엔드로 함께 보내 Gemini 응답이 문맥을 참고하도록 합니다.")
st.code(f"POST {API_BASE_URL}{CHAT_ENDPOINT}", language="text")

if "context_messages" not in st.session_state:
    st.session_state["context_messages"] = []

with st.sidebar:
    st.subheader("대화 상태")
    st.write(f"저장된 메시지 수: {len(st.session_state['context_messages'])}")
    st.write(f"백엔드로 함께 보낼 최근 메시지 수: 최대 {HISTORY_LIMIT}개")
    st.button("대화 초기화", on_click=reset_messages)
    st.warning("이 예제는 백엔드 설정에 따라 실제 Gemini API 호출이 발생할 수 있습니다.")

for message in st.session_state["context_messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        metadata = message.get("metadata")
        if metadata:
            st.caption(
                f"provider={metadata['provider']} | "
                f"model={metadata['model']} | "
                f"history_sent={metadata['history_sent']} | "
                f"actual_api_called={metadata['actual_api_called']}"
            )

prompt = st.chat_input("이전 대화를 이어서 질문해 보세요")

if prompt:
    # 현재 질문을 추가하기 전에, 이미 쌓여 있던 최근 대화 이력을 백엔드 전송용으로 준비합니다.
    # 이렇게 해야 현재 질문이 messages에 중복으로 들어가지 않습니다.
    recent_history = to_backend_history(st.session_state["context_messages"])

    st.session_state["context_messages"].append(
        {
            "role": "user",
            "content": prompt,
            "metadata": None,
        }
    )

    try:
        with st.spinner("최근 대화 이력을 함께 보내 Gemini 응답을 생성하는 중입니다..."):
            result = call_gemini_chat_api(prompt, recent_history)

        st.session_state["context_messages"].append(
            {
                "role": "assistant",
                "content": result["answer"],
                "metadata": {
                    "provider": result["provider"],
                    "model": result["model"],
                    "history_sent": len(recent_history),
                    "actual_api_called": result["actual_api_called"],
                },
            }
        )

    except httpx.ConnectError:
        st.session_state["context_messages"].append(
            {
                "role": "assistant",
                "content": "챗봇 백엔드에 연결할 수 없습니다. 05_ai-chatbot-interface/00_sample_backend를 먼저 실행하세요.",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "history_sent": len(recent_history),
                    "actual_api_called": False,
                },
            }
        )
    except httpx.TimeoutException:
        st.session_state["context_messages"].append(
            {
                "role": "assistant",
                "content": "Gemini 응답 시간이 초과되었습니다. 잠시 후 다시 시도하세요.",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "history_sent": len(recent_history),
                    "actual_api_called": False,
                },
            }
        )
    except httpx.HTTPStatusError as error:
        st.session_state["context_messages"].append(
            {
                "role": "assistant",
                "content": f"백엔드 API 오류가 발생했습니다. status={error.response.status_code}\n\n{error.response.text}",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "history_sent": len(recent_history),
                    "actual_api_called": False,
                },
            }
        )

    st.rerun()
