r"""챗봇 화면입니다.

개발할 때:
    1. PowerShell에서 `streamlit run .\app.py`를 실행합니다.
    2. 브라우저 왼쪽 사이드바에서 이 화면을 선택합니다.
    3. 이 파일을 수정한 뒤 Streamlit의 Rerun으로 확인합니다.
"""

import streamlit as st

from frontend_common import auth_headers, init_state, render_sidebar, request_json, require_login


init_state()

st.title("1. 챗봇")
st.caption("질문을 backend로 보내고, AI 답변을 화면에 대화 형식으로 표시합니다.")

with st.sidebar:
    render_sidebar()

with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("질문을 입력하세요.", placeholder="예: 오늘 학습한 내용을 요약해줘.")
    chat_submit = st.form_submit_button("전송", type="primary")

if chat_submit:
    user_message = user_message.strip()
    if not user_message:
        st.warning("질문을 입력하세요.")
    elif require_login():
        st.session_state["messages"].append({"role": "user", "content": user_message})

        with st.spinner("AI 응답을 생성하는 중입니다..."):
            data, error = request_json(
                "POST",
                "/chat",
                headers=auth_headers(),
                json={"message": user_message},
            )

        if error:
            st.error(error)
        else:
            answer = data["answer"]
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.caption(
                f"provider={data['provider']}, model={data['model']}, "
                f"actual_api_called={data['actual_api_called']}"
            )

st.divider()
st.subheader("대화 내용")

if not st.session_state["messages"]:
    st.info("아직 대화가 없습니다. 위 입력창에 질문을 입력해 보세요.")
else:
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
