import streamlit as st
from streamlit_local_storage import LocalStorage


storage = LocalStorage(key="login_storage")
stored_loginout = storage.getItem("loginout") or "logout"

# 새 브라우저 세션에서는 localStorage의 상태를 가져옵니다.
if "loginout" not in st.session_state:
    st.session_state.loginout = stored_loginout


def login():
    if (
        st.session_state.login_id == "id01"
        and st.session_state.login_pwd == "pwd01"
    ):
        st.session_state.loginout = "login"


def logout():
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_pwd = ""


# 현재 로그인 상태와 브라우저 저장값이 다를 때만 기록합니다.
if st.session_state.loginout != stored_loginout:
    storage.setItem(
        "loginout",
        st.session_state.loginout,
        key=f"save_{st.session_state.loginout}",
    )


if st.session_state.loginout == "logout":
    st.title("LOGIN")

    with st.form("login_form"):
        st.text_input("ID 입력", key="login_id")
        st.text_input("PWD 입력", type="password", key="login_pwd")
        st.form_submit_button("LOGIN", on_click=login)

else:
    st.success("로그인되었습니다.")
    st.button("LOGOUT", on_click=logout)
