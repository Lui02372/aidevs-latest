import os  # 운영체제 환경변수에서 API 주소를 읽기 위해 os 모듈을 가져옵니다.

import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")  # .env에 API_BASE_URL이 있으면 사용하고, 없으면 로컬 주소를 사용합니다.
CHAT_ENDPOINT = "/api/chat/mock"  # 실제 호출 경로를 변수로 분리해 나중에 경로가 바뀌어도 한 곳만 수정합니다.


def call_chat_api(message):
    """API 주소와 엔드포인트를 설정값으로 분리한 mock chat API 호출 함수입니다."""
    url = f"{API_BASE_URL}{CHAT_ENDPOINT}"  # API 기본 주소와 엔드포인트를 합쳐 실제 요청 URL을 만듭니다.
    response = httpx.post(url, json={"question": message}, timeout=5.0)  # mock chat API가 요구하는 question 필드로 질문을 보냅니다.
    response.raise_for_status()  # HTTP 상태 코드가 오류이면 예외를 발생시켜 실패를 명확히 처리합니다.
    return response.json()["answer"]  # 응답 JSON에서 assistant 답변 문자열만 꺼내 돌려줍니다.


st.title("챗 서비스 설정 분리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
st.caption(f"API 주소: {API_BASE_URL}{CHAT_ENDPOINT}")  # 현재 호출할 API 주소를 화면에 표시해 설정값을 확인합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 질문을 입력했을 때만 아래 로직을 실행합니다.
    st.chat_message("user").write(prompt)  # 사용자 질문을 user 말풍선에 출력합니다.
    st.chat_message("assistant").write(call_chat_api(prompt))  # 백엔드 mock API 응답을 assistant 말풍선에 출력합니다.
