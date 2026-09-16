import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.


def call_chat_api(message):
    """연결 실패와 타임아웃을 연습하기 위해 mock chat API를 호출합니다."""
    payload = {"question": message}  # 백엔드가 기대하는 요청 본문 구조에 맞춰 사용자 질문을 담습니다.
    response = httpx.post(f"{API_BASE_URL}/api/chat/mock", json=payload, timeout=3.0)  # mock chat API를 호출합니다.
    response.raise_for_status()  # HTTP 상태 코드가 오류이면 예외를 발생시켜 실패를 명확히 처리합니다.
    return response.json().get("answer", "응답에 answer 항목이 없습니다.")  # answer 값이 없을 때도 화면이 멈추지 않게 기본 문장을 돌려줍니다.


st.title("mock 챗 API 오류 처리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
st.caption("백엔드 연결 실패, 응답 지연, HTTP 오류를 사용자에게 어떻게 안내할지 연습합니다.")  # 실습 목적을 안내합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.chat_message("user").write(prompt)  # 사용자 질문을 user 말풍선에 출력합니다.
    try:
        reply = call_chat_api(prompt)  # 백엔드 mock API 응답을 받아 변수에 저장합니다.
        st.chat_message("assistant").write(reply)  # assistant 답변을 화면에 출력합니다.
    except httpx.HTTPStatusError as e:  # HTTP 상태 코드가 4xx 또는 5xx일 때 발생하는 예외를 처리합니다.
        st.error(f"Gemini가 바빠요")  # 상태 코드와 응답 본문을 화면에 표시합니다.