r"""이름 입력과 관심 분야 선택을 연결하는 아주 단순한 단계형 입력 예제입니다.

실행 방법:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\02_user-input-state-management\04_simple-multi-step-form.py

이 예제의 핵심:
    - 1단계에서 이름을 입력합니다.
    - 다음 버튼을 누르면 2단계로 이동합니다.
    - 2단계에서 1단계에 입력한 이름이 유지되는지 확인합니다.

03_simple-step-progress.py와의 차이:
    - 03 예제는 입력값 없이 step만 바꿉니다.
    - 04 예제는 step 이동에 아주 간단한 입력값 저장을 더합니다.

05_multi-step-form.py와의 차이:
    - 04 예제는 최대한 단순하게 보여 주는 예제입니다.
    - 05 예제는 입력 중 값과 확정 값을 분리하고, 이전/초기화 흐름까지 다룹니다.
"""

import streamlit as st


st.title("간단한 단계형 입력")
st.caption("1단계에서 입력한 이름이 2단계에서도 유지되는지 확인합니다.")


if "step" not in st.session_state:
    st.session_state.step = 1

if "name" not in st.session_state:
    st.session_state.name = ""

if "topic" not in st.session_state:
    st.session_state.topic = "Streamlit"


if st.session_state.step == 1:
    st.subheader("1단계: 이름 입력")

    st.text_input("이름", key="name", placeholder="예: 홍길동")

    if st.button("다음"):
        if st.session_state.name.strip():
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("이름을 입력하세요.")

else:
    st.subheader("2단계: 관심 분야 입력")

    st.session_state.topic = st.selectbox(
        "관심 분야",
        ["Streamlit", "FastAPI", "DB"],
        index=["Streamlit", "FastAPI", "DB"].index(st.session_state.topic),
    )

    st.write("이름:", st.session_state.name)
    st.write("관심 분야:", st.session_state.topic)

    if st.button("이전"):
        st.session_state.step = 1
        st.rerun()


st.divider()
st.subheader("현재 session_state 확인")
st.json(
    {
        "step": st.session_state.step,
        "name": st.session_state.name,
        "topic": st.session_state.topic,
    }
)
