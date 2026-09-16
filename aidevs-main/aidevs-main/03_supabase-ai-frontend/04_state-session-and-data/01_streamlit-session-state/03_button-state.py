import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("버튼 결과 상태")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "checked" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.checked = False  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

if st.button("확인 완료"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.session_state.checked = True  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

if st.session_state.checked:  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.success("확인 완료 상태입니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.info("확인 버튼을 눌러 상태를 바꾸세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

