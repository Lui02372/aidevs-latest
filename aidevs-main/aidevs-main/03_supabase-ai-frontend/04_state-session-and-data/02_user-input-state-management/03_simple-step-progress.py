r"""step 값만으로 화면 단계를 바꾸는 가장 단순한 예제입니다.

실행 방법:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\02_user-input-state-management\03_simple-step-progress.py

이 예제의 핵심:
    - `step`은 현재 화면이 몇 번째 단계인지 저장하는 값입니다.
    - 버튼을 누르면 `step` 값이 바뀝니다.
    - `step` 값에 따라 화면에 보이는 내용이 달라집니다.

왜 이 예제를 먼저 보나요?
    다음 예제인 `04_simple-multi-step-form.py`는 단계 이동에
    간단한 입력값 저장을 함께 다룹니다.

    이 파일에서는 입력값 저장을 거의 다루지 않고,
    "step 상태가 화면 흐름을 바꾼다"는 핵심만 먼저 연습합니다.
"""

import streamlit as st


st.title("간단한 단계 이동")
st.caption("step 값만 바꿔서 화면이 1단계, 2단계, 3단계로 바뀌는지 확인합니다.")


# step은 현재 몇 번째 화면을 보여 줄지 저장하는 상태입니다.
# Streamlit은 버튼을 누를 때마다 파일을 다시 실행하므로,
# 현재 단계를 일반 변수에만 저장하면 다음 실행에서 값이 사라집니다.
if "step" not in st.session_state:
    st.session_state.step = 1


def go_next() -> None:
    """다음 단계로 이동합니다."""

    if st.session_state.step < 3:
        st.session_state.step += 1


def go_previous() -> None:
    """이전 단계로 이동합니다."""

    if st.session_state.step > 1:
        st.session_state.step -= 1


def reset_step() -> None:
    """처음 단계로 돌아갑니다."""

    st.session_state.step = 1


st.write("현재 단계:", st.session_state.step)

if st.session_state.step == 1:
    st.subheader("1단계")
    st.write("첫 번째 화면입니다. 아직 입력값 저장은 다루지 않습니다.")
elif st.session_state.step == 2:
    st.subheader("2단계")
    st.write("두 번째 화면입니다. step 값이 바뀌어서 다른 내용이 보입니다.")
else:
    st.subheader("3단계")
    st.write("마지막 화면입니다. 처음으로 돌아가거나 이전 단계로 이동할 수 있습니다.")

col_prev, col_next, col_reset = st.columns(3)

with col_prev:
    st.button("이전", on_click=go_previous, disabled=st.session_state.step == 1)

with col_next:
    st.button("다음", type="primary", on_click=go_next, disabled=st.session_state.step == 3)

with col_reset:
    st.button("처음", on_click=reset_step)

st.divider()
st.subheader("현재 session_state 확인")
st.json({"step": st.session_state.step})
