import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("설문 폼 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.form("class_survey"):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    name = st.text_input("이름")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    difficulty = st.selectbox("오늘 수업 난이도", ["쉬움", "보통", "어려움"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    score = st.slider("이해도", 1, 5, 3)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    submitted = st.form_submit_button("제출")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if submitted:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.write(f"이름: {name}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    st.write(f"난이도: {difficulty}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    st.write(f"이해도: {score}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

