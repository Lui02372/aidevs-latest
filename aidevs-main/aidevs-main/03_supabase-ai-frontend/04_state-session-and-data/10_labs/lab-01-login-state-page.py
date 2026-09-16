import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("로그인 상태 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "access_token" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.access_token = None  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

username = st.text_input("사용자", value="student")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
password = st.text_input("비밀번호", type="password", value="1234")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if st.button("로그인"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    response = httpx.post(f"{API_BASE_URL}/api/login", json={"username": username, "password": password}, timeout=5.0)  # POST 요청의 응답을 response 변수에 저장해 성공 여부와 결과 데이터를 확인합니다.
    if response.status_code == 200:  # HTTP 응답 상태 코드를 확인해 성공과 실패 흐름을 나눕니다.
        st.session_state.access_token = response.json()["access_token"]  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

st.write("로그인 여부:", st.session_state.access_token is not None)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

