import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

if "messages" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.messages = []  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.


def call_chat_api(message):
    """05_ai-chatbot-interface 샘플 백엔드의 mock chat API를 호출합니다."""
    payload = {"question": message}  # 샘플 백엔드는 question 필드로 사용자 질문을 받습니다.
    response = httpx.post(f"{API_BASE_URL}/api/chat/mock", json=payload, timeout=5.0)  # mock chat API에 질문을 보냅니다.
    response.raise_for_status()  # HTTP 상태 코드가 4xx/5xx이면 예외를 발생시켜 실패를 명확히 처리합니다.
    return response.json()["answer"]  # 응답 JSON에서 assistant 답변 문자열만 꺼내 화면 코드로 돌려줍니다.


st.title("백엔드 mock 챗 API 클라이언트")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
st.caption("05_ai-chatbot-interface/00_sample_backend의 /api/chat/mock 엔드포인트를 호출합니다.")  # 호출 대상을 화면에 안내합니다.


for message in st.session_state.messages:  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    with st.chat_message(message["role"]):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
        st.write(message["content"])  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.session_state.messages.append({"role": "user", "content": prompt})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    reply = call_chat_api(prompt)  # 백엔드 또는 AI 서비스가 만든 응답 문자열을 화면 출력용 변수에 저장합니다.
    st.session_state.messages.append({"role": "assistant", "content": reply})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.rerun()  # session_state 변경 사항을 즉시 반영하기 위해 Streamlit 스크립트를 다시 실행합니다.

