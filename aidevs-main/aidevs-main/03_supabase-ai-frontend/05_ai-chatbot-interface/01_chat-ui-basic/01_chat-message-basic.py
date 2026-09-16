import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("기본 채팅 메시지")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.chat_message("user"):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.write("안녕하세요. Streamlit 챗봇 UI를 배우고 싶습니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

with st.chat_message("assistant"):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.write("좋습니다. 먼저 메시지 출력 구조부터 살펴보겠습니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.


