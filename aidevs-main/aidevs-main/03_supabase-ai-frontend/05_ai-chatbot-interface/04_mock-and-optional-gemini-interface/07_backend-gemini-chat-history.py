r"""백엔드 Gemini chat API 응답을 대화 이력으로 누적하는 Streamlit 예제입니다.

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
    streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\07_backend-gemini-chat-history.py

주의:
    이 예제는 질문을 보낼 때마다 백엔드의 /api/chat/gemini를 호출합니다.
    백엔드에 GEMINI_API_KEY가 설정되어 있으면 실제 Gemini API 호출이 발생할 수 있습니다.
    Gemini API key는 Streamlit 프론트엔드가 아니라 05_ai-chatbot-interface/00_sample_backend/.env에 둡니다.
"""

import os  # API_BASE_URL을 환경변수에서 읽기 위해 사용합니다.

import httpx  # FastAPI 백엔드 API에 HTTP 요청을 보내기 위해 사용합니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
CHAT_ENDPOINT = "/api/chat/gemini"


def reset_messages():
    """현재 화면에 저장된 대화 이력을 모두 삭제합니다."""

    st.session_state["gemini_messages"] = []


def call_gemini_chat_api(message):
    """FastAPI 백엔드의 Gemini chat API를 호출하고 응답 JSON을 반환합니다."""

    # Streamlit은 Gemini SDK를 직접 import하지 않습니다.
    # 화면은 질문만 백엔드로 보내고, 실제 Gemini API key와 호출 처리는 백엔드가 담당합니다.
    payload = {"question": message}
    response = httpx.post(f"{API_BASE_URL}{CHAT_ENDPOINT}", json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()


st.title("백엔드 Gemini 대화 이력 예제")
st.caption("Streamlit은 /api/chat/gemini 백엔드 API를 호출하고, 응답을 화면 대화 이력에 누적합니다.")
st.code(f"POST {API_BASE_URL}{CHAT_ENDPOINT}", language="text")

if "gemini_messages" not in st.session_state:
    # 각 메시지는 role, content, metadata를 가진 dict로 저장합니다.
    # metadata에는 provider, model, 실제 API 호출 여부 같은 부가 정보를 넣습니다.
    st.session_state["gemini_messages"] = []

with st.sidebar:
    st.subheader("대화 상태")
    st.write(f"저장된 메시지 수: {len(st.session_state['gemini_messages'])}")
    st.button("대화 초기화", on_click=reset_messages)
    st.warning("이 예제는 백엔드 설정에 따라 실제 Gemini API 호출이 발생할 수 있습니다.")

# 지금까지 저장된 메시지를 먼저 화면에 모두 출력합니다.
for message in st.session_state["gemini_messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        metadata = message.get("metadata")
        if metadata:
            st.caption(
                f"provider={metadata['provider']} | "
                f"model={metadata['model']} | "
                f"actual_api_called={metadata['actual_api_called']}"
            )

prompt = st.chat_input("Gemini에게 보낼 질문을 입력하세요")

if prompt:
    # 사용자 질문을 먼저 대화 이력에 저장합니다.
    st.session_state["gemini_messages"].append(
        {
            "role": "user",
            "content": prompt,
            "metadata": None,
        }
    )

    try:
        with st.spinner("백엔드에서 Gemini 응답을 생성하는 중입니다..."):
            result = call_gemini_chat_api(prompt)

        # 백엔드가 돌려준 Gemini 응답을 assistant 메시지로 저장합니다.
        st.session_state["gemini_messages"].append(
            {
                "role": "assistant",
                "content": result["answer"],
                "metadata": {
                    "provider": result["provider"],
                    "model": result["model"],
                    "actual_api_called": result["actual_api_called"],
                },
            }
        )

    except httpx.ConnectError:
        st.session_state["gemini_messages"].append(
            {
                "role": "assistant",
                "content": "챗봇 백엔드에 연결할 수 없습니다. 05_ai-chatbot-interface/00_sample_backend를 먼저 실행하세요.",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "actual_api_called": False,
                },
            }
        )
    except httpx.TimeoutException:
        st.session_state["gemini_messages"].append(
            {
                "role": "assistant",
                "content": "Gemini 응답 시간이 초과되었습니다. 잠시 후 다시 시도하세요.",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "actual_api_called": False,
                },
            }
        )
    except httpx.HTTPStatusError as error:
        st.session_state["gemini_messages"].append(
            {
                "role": "assistant",
                "content": f"백엔드 API 오류가 발생했습니다. status={error.response.status_code}\n\n{error.response.text}",
                "metadata": {
                    "provider": "error",
                    "model": "none",
                    "actual_api_called": False,
                },
            }
        )

    # 새 메시지를 저장한 뒤 화면을 다시 실행해 전체 대화가 위에서 순서대로 다시 그려지게 합니다.
    st.rerun()
