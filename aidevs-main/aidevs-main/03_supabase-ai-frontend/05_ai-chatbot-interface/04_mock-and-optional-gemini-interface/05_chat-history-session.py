r"""대화 내용이 화면에 계속 누적되는 챗봇 UI 예제입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\05_chat-history-session.py

이 예제는 Gemini/OpenAI API를 직접 호출하지 않습니다.
프론트엔드 화면에서는 대화 UI와 대화 이력 표시 흐름만 연습하고,
실제 LLM API 호출은 FastAPI 백엔드에서 처리하는 구조로 확장합니다.
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


def create_mock_reply(prompt):
    """사용자 질문을 받아 임시 assistant 응답을 만듭니다."""

    # 지금은 실제 AI API를 호출하지 않고, 화면 흐름을 확인하기 위한 mock 응답만 반환합니다.
    # 나중에는 이 함수 안에서 직접 Gemini를 호출하지 않고 FastAPI 백엔드 API를 호출하도록 바꿉니다.
    return f"mock 응답입니다. 사용자가 입력한 질문은 '{prompt}'입니다."


def reset_messages():
    """현재 화면에 저장된 대화 내용을 모두 삭제합니다."""

    # st.session_state는 Streamlit 앱이 다시 실행되어도 유지되는 임시 저장 공간입니다.
    # 여기서는 messages 리스트를 빈 리스트로 바꿔 대화 내용을 초기화합니다.
    st.session_state["messages"] = []


st.title("대화 이력 누적 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
st.caption("Gemini를 직접 호출하지 않고, 화면에 대화가 계속 쌓이는 구조만 연습합니다.")

# messages는 대화 전체를 저장하는 리스트입니다.
# 앱이 처음 실행될 때는 값이 없으므로 빈 리스트를 만들어 둡니다.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.sidebar:  # 화면 왼쪽 사이드바에는 현재 상태와 초기화 버튼을 배치합니다.
    st.subheader("대화 상태")
    st.write(f"저장된 메시지 수: {len(st.session_state['messages'])}")
    st.button("대화 초기화", on_click=reset_messages)

# 먼저 지금까지 저장된 메시지를 화면에 모두 출력합니다.
# role 값이 user이면 사용자 말풍선, assistant이면 assistant 말풍선으로 표시됩니다.
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자의 질문을 받습니다.

if prompt:  # 사용자가 질문을 입력하고 Enter를 누르면 아래 코드가 실행됩니다.
    user_message = {"role": "user", "content": prompt}
    assistant_message = {"role": "assistant", "content": create_mock_reply(prompt)}

    # 새 사용자 메시지와 assistant 응답을 session_state에 순서대로 추가합니다.
    # 이렇게 저장해 두면 Streamlit이 다시 실행되어도 이전 대화가 화면에 계속 출력됩니다.
    st.session_state["messages"].append(user_message)
    result = create_mock_reply(prompt)  # 실제 Gemini API 호출은 하지 않고, 화면 흐름만 확인합니다.
    st.session_state["messages"].append(assistant_message)

    # 메시지를 추가한 뒤 화면을 다시 실행해, 위쪽의 for문에서 전체 대화가 다시 그려지게 합니다.
    st.rerun()
