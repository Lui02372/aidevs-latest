# pip install streamlit-local-storage

import streamlit as st
from streamlit_session_browser_storage import SessionStorage


st.title("버튼 클릭 예제")

# 브라우저 localStorage를 사용합니다.
storage = SessionStorage()

# localStorage에서 저장된 값을 가져옵니다.
saved_sub_bt = storage.getItem(
    "sub_bt")

# session_state 기본값을 만듭니다.
if "sub_bt" not in st.session_state:
    st.session_state.sub_bt = False

# localStorage에 true가 저장되어 있으면 상태를 복원합니다.
if saved_sub_bt in ("true", True):
    st.session_state.sub_bt = True


message_col, alert_col = st.columns(2)

with message_col:
    clicked = st.button("인사말 보기")

with alert_col:
    alerted = st.button("인사말 보기 없애기")


if alerted:
    # 현재 세션의 상태를 변경합니다.
    st.session_state.sub_bt = False

    # 브라우저에 false를 저장합니다.
    storage.setItem("sub_bt", "false")


if clicked:
    st.info("인사말 보기 클릭")

    # 현재 세션의 상태를 변경합니다.
    st.session_state.sub_bt = True

    # 브라우저에 true를 저장합니다.
    storage.setItem("sub_bt", "true")


if st.session_state.sub_bt:
    st.success("Sub Button")

    sub_clicked = st.button("Sub Button")

    if sub_clicked:
        st.info("Sub Button이 클릭되었습니다.")