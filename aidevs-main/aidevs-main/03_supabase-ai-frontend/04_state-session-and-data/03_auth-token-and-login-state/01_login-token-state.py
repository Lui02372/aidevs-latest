import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("로그인 토큰 상태")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if "access_token" not in st.session_state:  # session_state에 값이 없을 때만 초기값을 만들어 화면 재실행에도 상태를 유지합니다.
    st.session_state.access_token = None  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.

if "login_response" not in st.session_state:  # 로그인 성공 후 서버가 내려준 응답 내용을 화면에 다시 보여 주기 위한 저장 공간입니다.
    st.session_state.login_response = None  # 아직 로그인하지 않은 상태이므로 처음에는 응답 데이터가 없습니다.

username = st.text_input("사용자 이름", value="student")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
password = st.text_input("비밀번호", type="password", value="1234")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if st.button("로그인"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    response = httpx.post(f"{API_BASE_URL}/api/login", json={"username": username, "password": password}, timeout=5.0)  # POST 요청의 응답을 response 변수에 저장해 성공 여부와 결과 데이터를 확인합니다.
    if response.status_code == 200:  # HTTP 응답 상태 코드를 확인해 성공과 실패 흐름을 나눕니다.
        data = response.json()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
        st.session_state.access_token = data["access_token"]  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
        st.session_state.username = data["username"]  # Streamlit이 재실행되어도 유지해야 하는 화면 상태를 session_state에 저장하거나 읽습니다.
        st.session_state.login_response = data  # 서버에서 받은 로그인 응답 전체를 보관해 토큰 구조를 화면에서 확인합니다.
        st.success("로그인 성공")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.error("로그인 실패")  # 오류 상황을 사용자에게 명확히 보여줍니다.

st.write("로그인 상태:", st.session_state.access_token is not None)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if st.session_state.login_response is not None:  # 로그인에 성공한 뒤에만 서버 응답 정보를 화면에 출력합니다.
    st.subheader("서버에서 받은 토큰 정보")  # 로그인 응답 중 토큰과 관련된 값을 확인하는 영역 제목입니다.
    st.write("access_token:", st.session_state.login_response["access_token"])  # 백엔드가 발급한 access token 값을 보여줍니다.
    st.write("token_type:", st.session_state.login_response["token_type"])  # Authorization header에서 사용할 token 종류를 보여줍니다.
    st.write("username:", st.session_state.login_response["username"])  # token이 어떤 사용자 로그인 결과인지 확인합니다.
    st.code(st.session_state.login_response["swagger_authorization_value"])  # Swagger Authorize 버튼에 입력할 값을 복사하기 쉽게 표시합니다.

