import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("상태 초기화 버튼")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "memo" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.memo = ""  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

st.session_state.memo = st.text_area("메모", value=st.session_state.memo)  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

if st.button("메모 초기화"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.session_state.memo = ""  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
    st.rerun()  # session_state 변경 사항을 즉시 반영하기 위해 Streamlit 스크립트를 다시 실행합니다.

st.write("현재 메모:", st.session_state.memo)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

