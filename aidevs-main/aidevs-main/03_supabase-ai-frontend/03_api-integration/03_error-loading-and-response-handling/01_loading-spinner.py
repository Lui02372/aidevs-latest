import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("로딩 상태 처리")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if st.button("API 호출"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    with st.spinner("백엔드 응답을 기다리는 중입니다..."):  # API 응답을 기다리는 동안 로딩 메시지를 보여주는 컨텍스트를 엽니다.
        response = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)  # GET 요청의 응답을 response 변수에 저장해 상태 코드와 JSON 데이터를 확인합니다.
    if response.status_code == 200:
        st.success("응답을 받았습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
        st.json(response.json())  # 딕셔너리나 JSON 응답을 보기 쉬운 구조로 화면에 표시합니다.
    else:
        st.warning("문제 발생")
