r"""Chat 화면입니다."""

import streamlit as st

from frontend_common import render_login_sidebar, require_login


st.title("Chat")
st.caption("실제 LLM 호출 없이 챗봇 화면 흐름을 mock 답변으로 연습합니다.")

with st.sidebar:
    render_login_sidebar()

if require_login():
    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("메시지", placeholder="예: Streamlit pages 구조를 설명해줘.")
        submitted = st.form_submit_button("전송")

    if submitted:
        message = message.strip()
        if not message:
            st.warning("메시지를 입력하세요.")
        else:
            st.session_state["chat_messages"].append({"role": "user", "content": message})
            st.session_state["chat_messages"].append(
                {
                    "role": "assistant",
                    "content": f"'{message}'에 대한 mock 답변입니다. 실제 backend 연결은 99 최종 프로젝트에서 진행합니다.",
                }
            )

    st.subheader("대화")
    if not st.session_state["chat_messages"]:
        st.info("아직 대화가 없습니다.")
    else:
        for item in st.session_state["chat_messages"]:
            st.chat_message(item["role"]).write(item["content"])
else:
    st.info("Chat 화면은 로그인 후 사용할 수 있습니다.")
