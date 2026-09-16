import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.
TOKEN = "sample-access-token"  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.title("캐시된 API 호출")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

@st.cache_data  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
def load_conversations(token):  # 반복해서 사용할 로직을 함수로 묶어 이름을 붙입니다.
    headers = {"Authorization": f"Bearer {token}"}  # 인증 토큰 같은 HTTP 헤더 값을 딕셔너리로 구성합니다.
    response = httpx.get(f"{API_BASE_URL}/api/conversations", headers=headers, timeout=5.0)  # GET 요청의 응답을 response 변수에 저장해 상태 코드와 JSON 데이터를 확인합니다.
    return response.json().get("items", [])  # 함수 실행 결과를 호출한 위치로 돌려줍니다.

st.dataframe(load_conversations(TOKEN))  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.

