import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("캐시 초기화")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

@st.cache_data  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
def get_numbers():  # 저장된 데이터를 조회하는 요청을 처리합니다.
    return [1, 2, 3, 4, 5]  # 함수 실행 결과를 호출한 위치로 돌려줍니다.

st.write(get_numbers())  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if st.button("캐시 비우기"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.cache_data.clear()  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    st.success("캐시를 비웠습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.

