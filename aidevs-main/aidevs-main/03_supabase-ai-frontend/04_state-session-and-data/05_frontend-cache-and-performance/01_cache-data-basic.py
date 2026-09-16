import time  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("cache_data 기본")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

@st.cache_data  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
def load_data():  # 반복해서 사용할 로직을 함수로 묶어 이름을 붙입니다.
    time.sleep(2)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    return ["Python", "Streamlit", "FastAPI"]  # 함수 실행 결과를 호출한 위치로 돌려줍니다.

if st.button("데이터 불러오기"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.write(load_data())  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

