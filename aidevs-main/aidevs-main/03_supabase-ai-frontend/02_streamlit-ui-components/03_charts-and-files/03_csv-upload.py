import pandas as pd  # CSV 파일을 표 형태의 DataFrame으로 읽기 위해 pandas를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("CSV 업로드 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])  # 사용자가 업로드한 CSV 파일 객체를 저장합니다.

if uploaded_file is not None:  # 파일이 실제로 업로드된 경우에만 아래 코드를 실행합니다.
    df = pd.read_csv(uploaded_file)  # 업로드된 CSV 파일을 pandas DataFrame으로 읽어옵니다.
    st.success("CSV 파일을 읽었습니다.")  # 파일 읽기에 성공했음을 화면에 표시합니다.
    st.dataframe(df)  # CSV 내용을 표 형태로 확인합니다.
    st.write("행 개수:", len(df))  # 데이터가 몇 행인지 표시합니다.
    st.write("컬럼 목록:", list(df.columns))  # 이후 필터와 차트에 사용할 수 있는 컬럼 이름을 표시합니다.
else:  # 아직 파일이 업로드되지 않은 경우 안내 메시지를 표시합니다.
    st.info("CSV 파일을 선택하면 표가 표시됩니다.")  # 사용자가 다음에 해야 할 일을 안내합니다.
