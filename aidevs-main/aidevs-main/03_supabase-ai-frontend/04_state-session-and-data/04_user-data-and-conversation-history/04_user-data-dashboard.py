import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.
TOKEN = "sample-access-token"  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.title("사용자 데이터 대시보드")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

headers = {"Authorization": f"Bearer {TOKEN}"}  # 인증 토큰 같은 HTTP 헤더 값을 딕셔너리로 구성합니다.
me_response = httpx.get(f"{API_BASE_URL}/api/me", headers=headers, timeout=5.0)  # 지정한 URL로 GET 요청을 보내 데이터를 조회합니다.
conversation_response = httpx.get(f"{API_BASE_URL}/api/conversations", headers=headers, timeout=5.0)  # 지정한 URL로 GET 요청을 보내 데이터를 조회합니다.

user = me_response.json()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
items = conversation_response.json().get("items", [])  # API 응답 JSON에서 목록 데이터를 꺼내 화면 표시용 변수에 저장합니다.

st.metric("사용자", user["username"])  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.
st.metric("대화 수", len(items))  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.
st.dataframe(items)  # 표 형태의 데이터를 스크롤 가능한 DataFrame UI로 표시합니다.

