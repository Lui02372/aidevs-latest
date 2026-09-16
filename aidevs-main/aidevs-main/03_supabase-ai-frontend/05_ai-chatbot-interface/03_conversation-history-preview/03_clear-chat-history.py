import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("대화 이력 초기화")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "messages" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.messages = []  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

if st.sidebar.button("대화 초기화"):  # 사용자가 버튼을 눌렀는지 True/False 값으로 확인합니다.
    st.session_state.messages = []  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.success("대화 이력을 초기화했습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.session_state.messages.append({"role": "user", "content": prompt})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.session_state.messages.append({"role": "assistant", "content": "임시 응답입니다."})  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

for message in st.session_state.messages:  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.chat_message(message["role"]).write(message["content"])  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.


