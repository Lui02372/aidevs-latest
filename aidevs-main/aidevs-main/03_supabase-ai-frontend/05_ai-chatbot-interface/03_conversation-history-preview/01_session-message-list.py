import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("세션 메시지 목록")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "messages" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.messages = []  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

st.write("현재 메시지 개수:", len(st.session_state.messages))  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if st.button("샘플 메시지 추가"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.session_state.messages.append({"role": "user", "content": "샘플 질문"})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.session_state.messages.append({"role": "assistant", "content": "샘플 응답"})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

for message in st.session_state.messages:  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.chat_message(message["role"]).write(message["content"])  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.


