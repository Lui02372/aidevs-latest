import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("간단 요약 통계")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

df = pd.DataFrame(  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.
    {
        "name": ["Kim", "Lee", "Park", "Choi"],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        "score": [70, 88, 95, 82],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        "study_time": [2.0, 3.5, 4.0, 3.0],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    }
)

average_score = df["score"].mean()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
max_score = df["score"].max()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
total_time = df["study_time"].sum()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.dataframe(df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.
mean_atra, max_area, total_area = st.columns(3)

with mean_atra:
    st.metric("평균 점수", f"{average_score:.1f}")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.
with max_area:
    st.metric("최고 점수", int(max_score))  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.
with total_area:
    st.metric("총 학습 시간", f"{total_time:.1f}시간")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

