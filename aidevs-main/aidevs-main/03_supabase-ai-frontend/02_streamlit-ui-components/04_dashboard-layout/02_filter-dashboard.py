import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


studendts =     [
        {"name": "Kim", "course": "Python", "score": 70},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        {"name": "Lee", "course": "Streamlit", "score": 88},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        {"name": "Park", "course": "Streamlit", "score": 95},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        {"name": "Choi", "course": "FastAPI", "score": 82},  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    ]

df = pd.DataFrame(studendts)

with st.sidebar:  # 화면 왼쪽 사이드바 영역에 입력 컴포넌트를 배치합니다.
    selected_course = st.selectbox("과정", ["전체"] + sorted(df["course"].unique()))  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    min_score = st.slider("최소 점수", 0, 100, 0)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
# -----------------------------------
st.title("필터 대시보드")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

filtered_df = df[df["score"] >= min_score]  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
if selected_course != "전체":  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    filtered_df = filtered_df[filtered_df["course"] == selected_course]  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.metric("필터 결과 수", len(filtered_df))  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.
st.dataframe(filtered_df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.
# 합과 평균
students_sum =  df["score"].sum()
students_avg =  df["score"].mean()
col_sum, col_avg = st.columns(2)  # 메인 화면을 여러 열로 나누어 대시보드 요소를 배치합니다.
with col_sum:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("합계", f"{students_sum}점")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

with col_avg:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("평균", f"{students_avg:.1f}점")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

