r"""목록을 조회할 때 사용할 필터 조건 상태를 저장하는 예제입니다.

실행 방법:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\04_state-session-and-data\02_user-input-state-management\02_filter-state.py

이 예제의 핵심:
    - `filters`는 "데이터를 어떤 조건으로 볼지"를 나타내는 상태입니다.
    - 과정, 점수, 상태값, 정렬 기준처럼 목록 조회 조건을 저장할 때 사용합니다.
    - 사용자가 필터를 적용하면 `st.session_state.filters`에 조건이 저장됩니다.
    - 이후 대화 이력 조회, 서비스 로그 대시보드, 운영 대시보드 필터로 확장할 수 있습니다.

01_profile-state.py와의 차이:
    - 01_profile-state.py는 "내 정보"를 저장합니다.
    - 02_filter-state.py는 "데이터를 어떤 조건으로 볼지"를 저장합니다.
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


st.title("필터 상태 관리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

# filters는 사용자 자체에 대한 정보가 아니라, 데이터 조회 조건을 담는 상태입니다.
# 예를 들어 대화 이력에서 "오류만 보기", 서비스 로그에서 "warning 이상만 보기" 같은 화면에 쓰입니다.
if "filters" not in st.session_state:
    st.session_state.filters = {"course": "전체", "min_score": 0}

course = st.selectbox("과정", ["전체", "Python", "Streamlit", "FastAPI"])
min_score = st.slider("최소 점수", 0, 100, st.session_state.filters["min_score"])

if st.button("필터 적용"):
    # 버튼을 누른 순간의 선택 조건을 filters 상태에 저장합니다.
    # 이후 목록 조회 API를 호출할 때 이 값을 query parameter나 요청 조건으로 사용할 수 있습니다.
    st.session_state.filters = {"course": course, "min_score": min_score}

st.write("현재 필터:", st.session_state.filters)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
