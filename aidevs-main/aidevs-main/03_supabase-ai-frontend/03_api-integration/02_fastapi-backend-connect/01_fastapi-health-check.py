import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("FastAPI 상태 확인")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if st.button("백엔드 상태 확인"):  # 버튼을 누른 순간에만 API 요청을 보냅니다.
    response = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)  # 백엔드 health check API에 GET 요청을 보냅니다.
    st.write("Status Code:", response.status_code)  # HTTP 상태 코드를 화면에 표시합니다.
    st.json(response.json())  # JSON 응답을 접고 펼칠 수 있는 형태로 화면에 표시합니다.
