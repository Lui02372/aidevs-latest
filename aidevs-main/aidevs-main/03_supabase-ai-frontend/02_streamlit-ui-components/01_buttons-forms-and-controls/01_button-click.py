import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("버튼 클릭 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "sub_bt" not in st.session_state:
    st.session_state.sub_bt  = False

message_col, alert_col = st.columns(2)  # 버튼 두 개를 나란히 배치하기 위해 화면을 두 칸으로 나눕니다.

with message_col:
    clicked = st.button("인사말 보기")  # 버튼을 누르면 True, 누르지 않으면 False가 됩니다.
with alert_col:
    alerted = st.button("인사말 보기 ") 

# ----------------------------------------------------------------
if alerted:
    st.session_state.sub_bt = False

if clicked: 
   st.info("인사말 보기 클릭")
   st.session_state.sub_bt = True

if st.session_state.sub_bt:
    st.success("sub Button")
    sub_clicked = st.button("Sub Button")
    if sub_clicked:
        st.info("sub button")

