import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


def call_mock_chat_service(message):  # 반복해서 사용할 로직을 함수로 묶어 이름을 붙입니다.
    return f"로컬 임시 응답입니다: {message}"  # 함수 실행 결과를 호출한 위치로 돌려줍니다.


st.title("로컬 AI 함수 분리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.chat_message("user").write(prompt)  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.
    reply = call_mock_chat_service(prompt)  # 백엔드 또는 AI 서비스가 만든 응답 문자열을 화면 출력용 변수에 저장합니다.
    st.chat_message("assistant").write(reply)  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.


