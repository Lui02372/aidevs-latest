r"""사용자 프로필 정보 상태를 저장하는 예제입니다.

실행 방법:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\02_user-input-state-management\01_profile-state.py

이 예제의 핵심:
    - `profile`은 "사용자가 누구인지"를 나타내는 상태입니다.
    - 이름, 역할, 관심 분야, 학습 목표처럼 사용자에 대한 정보를 저장할 때 사용합니다.
    - 화면이 다시 실행되어도 `st.session_state.profile`에 저장된 값은 유지됩니다.
    - 이후 로그인 사용자 정보, 마이페이지, 사용자 설정 화면으로 확장할 수 있습니다.

02_filter-state.py와의 차이:
    - 01_profile-state.py는 "내 정보"를 저장합니다.
    - 02_filter-state.py는 "데이터를 어떤 조건으로 볼지"를 저장합니다.
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


st.title("프로필 상태 관리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

# profile은 사용자 자체에 대한 정보를 담는 상태입니다.
# 예를 들어 로그인한 사용자의 이름, 역할, 선호 설정을 화면에 유지할 때 이런 방식이 쓰입니다.
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "", "role": "AI 개발자"}

name = st.text_input("이름", value=st.session_state.profile["name"])
role = st.selectbox(
    "역할",
    ["AI 개발자", "백엔드 개발자", "프론트엔드 개발자"],
    index=0,
)

if st.button("프로필 저장"):
    # 버튼을 누른 순간의 입력값을 profile 상태에 다시 저장합니다.
    # 저장 후에는 Streamlit이 다시 실행되어도 아래 JSON 출력에 같은 값이 유지됩니다.
    st.session_state.profile = {"name": name, "role": role}

st.json(st.session_state.profile)  # 딕셔너리나 JSON 응답을 보기 쉬운 구조로 화면에 표시합니다.
