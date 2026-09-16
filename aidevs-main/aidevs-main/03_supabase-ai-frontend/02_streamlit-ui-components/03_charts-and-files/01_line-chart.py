import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("선 그래프 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

df = pd.DataFrame(  # 딕셔너리 데이터를 행과 열을 가진 DataFrame 표 구조로 변환합니다.
    {
        "week": [1, 2, 3, 4],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
        "study_time": [3, 5, 4, 7],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    }
).set_index("study_time")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

# st.dataframe(df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.
st.line_chart(df)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

