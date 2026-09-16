r"""단계형 입력 화면에서 입력값까지 함께 유지하는 예제입니다.

실행 방법:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\02_user-input-state-management\05_multi-step-form.py

이 예제의 핵심:
    - `step`은 현재 사용자가 몇 번째 화면에 있는지 저장하는 상태입니다.
    - `name_input`은 1단계 입력창에 연결된 임시 입력 상태입니다.
    - `name`은 "다음 단계로 이동"을 눌렀을 때 확정 저장되는 이름입니다.
    - `topic`은 2단계에서 선택한 관심 분야입니다.

03_simple-step-progress.py와의 차이:
    - 03 예제는 step 값만 바꿔 화면이 바뀌는 흐름을 보여 줍니다.
    - 04 예제는 단계 이동에 입력값 저장까지 더합니다.

왜 name_input과 name을 나누나요?
    Streamlit 위젯의 key와 저장용 값을 같은 이름으로 쓰면,
    단계 전환이나 초기화 시점에 값이 헷갈릴 수 있습니다.

    그래서 이 예제에서는 다음처럼 역할을 나눕니다.

        name_input: 사용자가 현재 입력창에 쓰고 있는 값
        name: 1단계를 통과하면서 확정 저장한 값

    이렇게 하면 2단계로 넘어가도 이름이 사라지지 않습니다.
"""

import streamlit as st


st.title("단계형 입력 상태")
st.caption("step 상태와 입력값 상태를 함께 사용해 단계형 입력 화면을 만듭니다.")


if "step" not in st.session_state:
    st.session_state.step = 1

if "name_input" not in st.session_state:
    st.session_state.name_input = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "topic" not in st.session_state:
    st.session_state.topic = "Streamlit"

if "warning_message" not in st.session_state:
    st.session_state.warning_message = ""


def move_to_step_2() -> None:
    """1단계 입력값을 검증하고, 이름을 확정 저장한 뒤 2단계로 이동합니다."""

    name = st.session_state.name_input.strip()

    if not name:
        st.session_state.warning_message = "이름을 입력한 뒤 다음 단계로 이동하세요."
        return

    st.session_state.name = name
    st.session_state.warning_message = ""
    st.session_state.step = 2


def move_to_step_1() -> None:
    """2단계에서 1단계로 돌아갑니다."""

    st.session_state.step = 1


def reset_form() -> None:
    """단계와 입력값을 모두 초기화합니다."""

    st.session_state.step = 1
    st.session_state.name_input = ""
    st.session_state.name = ""
    st.session_state.topic = "Streamlit"
    st.session_state.warning_message = ""


if st.session_state.step == 1:
    st.subheader("1단계: 이름 입력")
    st.write("먼저 사용자의 이름을 입력합니다.")

    st.text_input("이름", key="name_input", placeholder="예: 홍길동")

    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    st.button("다음 단계로 이동", type="primary", on_click=move_to_step_2)

else:
    st.subheader("2단계: 관심 분야 선택")
    st.write("1단계에서 확정 저장한 이름을 2단계에서도 계속 사용합니다.")

    topics = ["Streamlit", "FastAPI", "DB"]
    selected_index = topics.index(st.session_state.topic)

    st.session_state.topic = st.selectbox(
        "관심 분야",
        topics,
        index=selected_index,
    )

    st.divider()
    st.write("입력 요약")
    st.write("이름:", st.session_state.name)
    st.write("관심 분야:", st.session_state.topic)

    col_prev, col_reset = st.columns(2)

    with col_prev:
        st.button("이전 단계로 이동", on_click=move_to_step_1)

    with col_reset:
        st.button("처음부터 다시 입력", on_click=reset_form)


st.divider()
st.subheader("현재 session_state 확인")
st.json(
    {
        "step": st.session_state.step,
        "name_input": st.session_state.name_input,
        "name": st.session_state.name,
        "topic": st.session_state.topic,
    }
)
