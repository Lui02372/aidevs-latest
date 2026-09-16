r"""회원가입 화면입니다.

개발 방법:
    streamlit run .\app.py 로 전체 앱을 실행한 뒤,
    브라우저 왼쪽 사이드바에서 이 화면을 선택합니다.
"""

import streamlit as st

from frontend_common import init_state, render_login_sidebar


init_state()

st.title("회원가입")
st.caption("실제 backend 없이 회원가입 화면 흐름만 연습합니다.")

with st.sidebar:
    render_login_sidebar()

with st.form("signup_form"):
    email = st.text_input("이메일", value="new-student@example.com")
    display_name = st.text_input("표시 이름", value="새 수강생")
    password = st.text_input("비밀번호", value="pass1234", type="password")
    agree = st.checkbox("서비스 이용 약관에 동의합니다.")
    submitted = st.form_submit_button("회원가입")

if submitted:
    if not email or not display_name or not password:
        st.warning("모든 항목을 입력하세요.")
    elif not agree:
        st.warning("약관 동의가 필요합니다.")
    else:
        st.session_state["registered_users"].append(
            {
                "email": email,
                "display_name": display_name,
            }
        )
        st.success("회원가입 화면 흐름이 완료되었습니다.")
        st.json({"email": email, "display_name": display_name})

st.subheader("현재 mock 가입 목록")
if st.session_state["registered_users"]:
    st.dataframe(st.session_state["registered_users"], use_container_width=True)
else:
    st.info("아직 가입한 사용자가 없습니다.")
