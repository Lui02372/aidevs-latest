import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("FastAPI 메시지 전송")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

name = st.text_input("이름")  # 사용자가 입력한 이름을 문자열로 저장합니다.
message = st.text_input("메시지")  # 백엔드에 보낼 메시지를 문자열로 저장합니다.

if st.button("전송"):  # 버튼을 누른 순간에만 POST 요청을 보냅니다.
    payload = {"name": name, "message": message}  # 백엔드 Pydantic 모델이 기대하는 JSON 구조로 데이터를 만듭니다.
    response = httpx.post(f"{API_BASE_URL}/api/message", json=payload, timeout=5.0)  # 메시지 API에 POST 요청을 보냅니다.

    st.info(f"응답코드: {response.status_code}")

    if response.status_code == 200:  # HTTP 상태 코드가 200이면 정상 응답으로 처리합니다.
        result = response.json()  # JSON 응답을 딕셔너리로 변환합니다.
        st.success(result["reply"])  # 백엔드가 만든 reply 값을 성공 메시지로 표시합니다.
    else:  # 200이 아닌 상태 코드는 실패로 보고 오류를 표시합니다.
        st.error(f"API 호출 실패: {response.status_code}")  # 오류 상황을 사용자에게 명확히 보여줍니다.
