from datetime import datetime  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("TTL 캐시 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

@st.cache_data(ttl=10)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
def get_current_time():  # 저장된 데이터를 조회하는 요청을 처리합니다.
    return datetime.now().strftime("%H:%M:%S")  # 함수 실행 결과를 호출한 위치로 돌려줍니다.

st.write("캐시된 시각:", get_current_time())  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.caption("10초 안에는 같은 값이 표시됩니다.")  # 보조 설명이나 현재 설정값을 작은 글씨로 표시합니다.

