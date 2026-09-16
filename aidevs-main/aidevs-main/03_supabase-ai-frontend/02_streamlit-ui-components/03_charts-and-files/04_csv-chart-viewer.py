import pandas as pd  # 목록 데이터를 표와 차트로 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("CSV 차트 뷰어")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

st.info(
    "연습용 CSV가 필요하면 "
    "02_streamlit-ui-components/03_charts-and-files/sample_data/sample-service-logs.csv 파일을 업로드해 보세요."
)  # 수강생이 바로 테스트할 수 있는 예제 파일 위치를 안내합니다.

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if uploaded_file is not None:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    df = pd.read_csv(uploaded_file)  # 업로드된 CSV 파일을 pandas DataFrame으로 읽어옵니다.
    st.dataframe(df)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.

    numeric_columns = list(df.select_dtypes(include="number").columns)  # DataFrame에서 숫자형 컬럼만 골라 차트 후보 목록을 만듭니다.

    if numeric_columns:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        selected_column = st.selectbox("차트로 볼 숫자 컬럼", numeric_columns)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
        st.line_chart(df[selected_column])  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.warning("차트로 표시할 숫자 컬럼이 없습니다.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.info("숫자 컬럼이 포함된 CSV 파일을 업로드하세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

