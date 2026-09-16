import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("숫자 입력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, value=20)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
next_year_age = age + 1  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"현재 나이는 {age}세입니다. {next_year_age}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.write(f"내년에는 {next_year_age}세가 됩니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

