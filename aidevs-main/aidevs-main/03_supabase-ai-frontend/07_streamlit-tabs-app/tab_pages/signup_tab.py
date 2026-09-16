"""회원가입 탭입니다."""

import streamlit as st


def render_signup_tab() -> None:
    """실제 backend 없이 회원가입 화면 흐름만 연습합니다."""

    st.subheader("회원가입")
    st.caption("실제 backend 없이 회원가입 화면 흐름만 연습합니다.")

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
            st.success("회원가입 화면 흐름을 완료했습니다.")
            st.json({"email": email, "display_name": display_name})

    st.subheader("현재 mock 가입 목록")
    if st.session_state["registered_users"]:
        st.dataframe(st.session_state["registered_users"], use_container_width=True)
    else:
        st.info("아직 가입한 사용자가 없습니다.")
