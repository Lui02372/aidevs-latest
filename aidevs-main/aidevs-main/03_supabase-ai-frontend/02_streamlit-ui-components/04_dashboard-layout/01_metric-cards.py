import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.
import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.

st.title("지표 카드 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

#----------------------------------------------
students = {
    "name": ["Kim", "Lee", "Park", "Choi"],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    "score": [70, 88, 95, 82],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    "complete": [80, 90, 65, 90],  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
}
#----------------------------------------------
df = pd.DataFrame(students)
# st.dataframe(df)

students_num = len(df["name"])
students_avg = df["score"].mean()
students_com = df["complete"].mean()

col_students, col_average, col_complete = st.columns(3)  # 메인 화면을 여러 열로 나누어 대시보드 요소를 배치합니다.

with col_students:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("수강생", f"{students_num}명")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

with col_average:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("평균 점수", f"{students_avg:.1f}점")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

with col_complete:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("완료율", f"{students_com:.1f}%")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

