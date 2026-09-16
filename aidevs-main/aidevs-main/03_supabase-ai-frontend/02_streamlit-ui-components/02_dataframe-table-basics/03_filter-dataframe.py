import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("DataFrame 필터링")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

df = pd.DataFrame(  # 여러 학생 정보를 행과 열을 가진 DataFrame 표 구조로 변환합니다.
    [
        {"name": "Kim", "course": "Python", "score": 70},  # 한 명의 학습자 데이터를 딕셔너리 한 개로 표현합니다.
        {"name": "Lee", "course": "Streamlit", "score": 88},  # 같은 키(name, course, score)를 사용해야 표의 컬럼이 일정해집니다.
        {"name": "Park", "course": "Streamlit", "score": 95},  # 이후 필터링에서 course와 score 컬럼을 사용합니다.
        {"name": "Choi", "course": "FastAPI", "score": 82},  # 작은 예제 데이터지만 API 응답 목록과 같은 형태로 볼 수 있습니다.
    ]
)

course = st.selectbox("과정 선택", sorted(df["course"].unique()))  # 중복을 제거한 과정 목록 중 하나를 선택합니다.
min_score = st.slider("최소 점수", min_value=0, max_value=100, value=80)  # 필터 기준이 될 최소 점수를 슬라이더로 선택합니다.

filtered_df = df[(df["course"] == course) & (df["score"] >= min_score)]  # 선택 과정과 최소 점수를 모두 만족하는 행만 남깁니다.

st.write("필터 결과")  # 아래 표가 어떤 데이터인지 설명합니다.
st.dataframe(filtered_df)  # 필터링된 결과를 스크롤 가능한 표로 표시합니다.
st.caption(f"총 {len(filtered_df)}개의 행이 조건에 맞습니다.")  # 필터 결과 개수를 함께 표시합니다.
