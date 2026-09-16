import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("폼 입력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.form("profile_form"):
    name = st.text_input("이름")  # 입력값은 st.session_state["profile_name"]에도 저장됩니다.
    age = st.number_input("나이",min_value=0, max_value=100, value=20)
    left_col , right_col  = st.columns(2)
    with left_col:
        submitted = st.form_submit_button("제출") 
    with right_col:
        reset = st.form_submit_button("초기화")  # 입력값을 기본값으로 되돌리는 버튼입니다.

if submitted:
    if name:
        st.info(f"{name} {age}")
    else:
        st.warning("이름을 입력 하세요")


