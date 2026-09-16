import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("기본 챗봇 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.chat_message("user").write(prompt)  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.
    st.chat_message("assistant").write("임시 응답입니다. 다음 단계에서 이력을 저장합니다.")  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.


