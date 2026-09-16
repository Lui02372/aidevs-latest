import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("폼 입력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.


def reset_profile_form():
    """폼 입력값을 처음 상태로 되돌립니다."""

    # Streamlit 입력 컴포넌트는 key를 지정하면 st.session_state에 값이 저장됩니다.
    # 초기화 버튼을 누르면 이 저장값을 직접 기본값으로 바꿉니다.
    st.session_state["profile_name"] = ""
    st.session_state["profile_role"] = "AI"


# 입력 컴포넌트가 처음 만들어지기 전에 기본값을 준비합니다.
# 이렇게 해두면 앱을 처음 실행했을 때도 name과 role의 시작값이 명확해집니다.
if "profile_name" not in st.session_state:
    st.session_state["profile_name"] = ""

if "profile_role" not in st.session_state:
    st.session_state["profile_role"] = "Backend"


with st.form("profile_form"):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    name = st.text_input("이름", key="profile_name")  # 입력값은 st.session_state["profile_name"]에도 저장됩니다.
    role = st.selectbox(
        "관심 분야",
        ["AI", "Backend", "Frontend", "Data"],
        key="profile_role",
    )  # 선택값은 st.session_state["profile_role"]에도 저장됩니다.

    submit_col, reset_col = st.columns(2)  # 버튼 두 개를 나란히 보여주기 위해 화면을 두 칸으로 나눕니다.

    with submit_col:
        submitted = st.form_submit_button("제출")  # 입력한 값을 확인하는 버튼입니다.

    with reset_col:
        reset = st.form_submit_button("초기화", on_click=reset_profile_form)  # 입력값을 기본값으로 되돌리는 버튼입니다.
#------------------------------------------------------------------------------------------------------------------------------------
if reset:  # 초기화 버튼을 눌렀을 때 실행합니다.
    st.info("입력값을 초기화했습니다.")  # 사용자에게 초기화가 완료되었음을 알려줍니다.
elif submitted:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    if name:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.success(f"{name}님의 관심 분야는 {role}입니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.error("이름을 입력하세요.")  # 오류 상황을 사용자에게 명확히 보여줍니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.info("값을 입력한 뒤 제출 버튼을 누르세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

