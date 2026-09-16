import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("선택 입력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

language = st.selectbox("관심 있는 언어를 선택하세요", ["Python", "JavaScript", "SQL"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
level = st.radio("현재 학습 수준을 선택하세요", ["입문", "기초", "중급"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"선택한 언어: {language}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.write(f"현재 수준: {level}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if language == "Python" and level == "입문":  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.info("Streamlit은 Python 입문자가 화면을 만들어 보기 좋은 도구입니다.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

