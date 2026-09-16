import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("DataFrame 만들기")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

students = [  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    {"name": "Kim", "course": "Streamlit", "score": 85},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    {"name": "Lee", "course": "FastAPI", "score": 78},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    {"name": "Park", "course": "Streamlit", "score": 92},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    {"name": "Park", "course": "Streamlit", "score": 92},
    {"name": "Park", "course": "Streamlit", "score": 92},
]

df = pd.DataFrame(students)  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.

st.write("원본 데이터")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.dataframe(df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.
# st.write("컬럼 목록:", list(df.columns))  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
st.write("컬럼 목록:", students)

