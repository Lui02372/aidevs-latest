import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("백엔드 mock 챗 클라이언트 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
st.caption("05_ai-chatbot-interface/00_sample_backend를 실행한 뒤 테스트합니다.")  # 실습 전 필요한 백엔드를 안내합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 질문을 입력했을 때만 아래 코드를 실행합니다.
    st.chat_message("user").write(prompt)  # 사용자 질문을 user 말풍선에 출력합니다.
    try:  # 백엔드 연결은 실패할 수 있으므로 try 블록에서 실행합니다.
        response = httpx.post(f"{API_BASE_URL}/api/chat/mock", json={"question": prompt}, timeout=5.0)  # mock chat API에 질문을 보냅니다.
        response.raise_for_status()  # HTTP 상태 코드가 오류이면 예외를 발생시켜 실패를 명확히 처리합니다.
        st.chat_message("assistant").write(response.json()["answer"])  # 응답 JSON의 answer 값을 assistant 말풍선에 출력합니다.
    except httpx.ConnectError:  # 백엔드 서버가 실행 중이 아니면 연결 오류가 발생합니다.
        st.error("백엔드 서버를 먼저 실행하세요.")
