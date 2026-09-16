import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.set_page_config(page_title="학습 진도 대시보드", layout="wide")  # 대시보드가 넓게 보이도록 페이지 레이아웃을 wide로 설정합니다.

df = pd.DataFrame(  # 학습자 목록을 DataFrame으로 만들어 표, 지표, 차트에 함께 사용합니다.
    [
        {"name": "Kim", "course": "Python", "progress": 75, "score": 80},  # 한 행은 한 명의 학습자 데이터를 의미합니다.
        {"name": "Lee", "course": "Streamlit", "progress": 90, "score": 88},  # course는 필터 조건으로 사용됩니다.
        {"name": "Park", "course": "Streamlit", "progress": 60, "score": 72},  # progress와 score는 지표와 차트에 사용됩니다.
        {"name": "Choi", "course": "FastAPI", "progress": 45, "score": 68},  # 이후 Supabase 조회 결과도 비슷한 목록 형태로 다룰 수 있습니다.
    ]
)

# with st.sidebar:  # 화면 왼쪽 사이드바에는 필터 조건을 배치합니다.
#     selected_course = st.selectbox("과정", ["전체"] + sorted(df["course"].unique()))  # 전체 또는 특정 과정을 선택합니다.
#     min_progress = st.slider("최소 진도율", 0, 100, 0)  # 표시할 데이터의 최소 진도율을 선택합니다.

st.title("학습 진도 대시보드")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

selected_course = st.selectbox("과정", ["전체"] + sorted(df["course"].unique()))  # 전체 또는 특정 과정을 선택합니다.
min_progress = st.slider("최소 진도율", 0, 100, 0)  # 표시할 데이터의 최소 진도율을 선택합니다.

filtered_df = df[df["progress"] >= min_progress]  # 먼저 최소 진도율 조건에 맞는 행만 남깁니다.
if selected_course != "전체":  # 특정 과정이 선택된 경우에는 과정 조건을 추가로 적용합니다.
    filtered_df = filtered_df[filtered_df["course"] == selected_course]  # 선택한 과정에 해당하는 행만 남깁니다.
#---------------------------------------------------------
col_count, col_progress, col_score = st.columns(3)  # 상단 지표 영역을 세 개의 열로 나눕니다.

with col_count:  # 첫 번째 열에는 필터 결과에 포함된 학습자 수를 표시합니다.
    st.metric("학습자 수", len(filtered_df))  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

with col_progress:  # 두 번째 열에는 평균 진도율을 표시합니다.
    average_progress = filtered_df["progress"].mean() if not filtered_df.empty else 0  # 데이터가 없으면 평균 대신 0을 사용합니다.
    st.metric("평균 진도율", f"{average_progress:.1f}%")  # 평균 진도율을 소수점 한 자리로 표시합니다.

with col_score:  # 세 번째 열에는 평균 점수를 표시합니다.
    average_score = filtered_df["score"].mean() if not filtered_df.empty else 0  # 데이터가 없으면 평균 대신 0을 사용합니다.
    st.metric("평균 점수", f"{average_score:.1f}")  # 평균 점수를 소수점 한 자리로 표시합니다.
#-------------------------------------------------------
tab_table, tab_chart = st.tabs(["학습자 목록", "진도 차트"])  # 표와 차트를 탭으로 나누어 화면을 깔끔하게 유지합니다.

with tab_table:  # 첫 번째 탭에는 필터링된 원본 데이터를 표로 표시합니다.
    st.dataframe(filtered_df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.

with tab_chart:  # 두 번째 탭에는 같은 데이터를 차트로 표시합니다.
    if not filtered_df.empty:  # 필터 결과가 있을 때만 차트를 만듭니다.
        chart_df = filtered_df.set_index("name")[["progress", "score"]]  # 이름을 기준 축으로 사용하고 진도율과 점수만 차트에 사용합니다.
        st.bar_chart(chart_df)  # 숫자 데이터를 막대 차트로 시각화합니다.
    else:  # 필터 조건에 맞는 데이터가 없으면 차트 대신 안내 메시지를 표시합니다.
        st.warning("필터 조건에 맞는 데이터가 없습니다.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.
