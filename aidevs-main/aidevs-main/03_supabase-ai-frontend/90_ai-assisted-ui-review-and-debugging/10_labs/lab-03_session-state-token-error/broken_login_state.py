r"""Lab 03. session_state와 token 처리 오류가 있는 예제입니다.

실행 명령:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-03_session-state-token-error\broken_login_state.py

프롬프트 예시:
    이 Streamlit 파일에서 로그인 token 저장과 Authorization header 구성을 리뷰해주세요.
    session_state 초기화, token 저장, header 형식, 로그아웃 처리를 기준으로 문제를 찾아주세요.
"""

import httpx
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.title("session_state token 오류 실습")

username = st.text_input("사용자 이름", value="student")
password = st.text_input("비밀번호", value="1234", type="password")

if st.button("로그인"):
    response = httpx.post(
        f"{API_BASE_URL}/api/login",
        json={"username": username, "password": password},
        timeout=5.0,
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state.access_token = data["access_token"]
        st.success("로그인 성공")
    else:
        st.error("로그인 실패")


# 의도적인 문제 1:
# access_token key가 아직 없을 수 있는데 바로 읽고 있습니다.
st.write("현재 token:", st.session_state.access_token)


if st.button("내 정보 조회"):
    # 의도적인 문제 2:
    # 백엔드는 Authorization: Bearer sample-access-token 형식을 기대합니다.
    # 아래 코드는 header 이름과 값의 형식이 모두 잘못되어 있습니다.
    headers = {"Token": st.session_state.access_token}
    response = httpx.get(f"{API_BASE_URL}/api/me", headers=headers, timeout=5.0)
    st.write("HTTP status code:", response.status_code)
    st.json(response.json())


if st.button("로그아웃"):
    st.session_state.access_token = None
    st.info("로그아웃했습니다.")
