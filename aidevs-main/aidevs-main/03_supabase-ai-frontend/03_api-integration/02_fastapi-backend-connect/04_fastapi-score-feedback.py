import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("점수 피드백 API 연동")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

name = st.text_input("이름")  # 사용자가 입력한 이름을 문자열로 저장합니다.
score = st.slider("점수", min_value=0, max_value=100, value=70)  # 0부터 100 사이의 점수를 선택합니다.

if st.button("피드백 요청"):  # 버튼을 누른 순간에만 POST 요청을 보냅니다.
    payload = {"name": name, "score": score}  # 백엔드에 보낼 JSON 요청 본문을 만듭니다.
    response = httpx.post(f"{API_BASE_URL}/api/score-feedback", json=payload, timeout=5.0)  # 점수 피드백 API에 POST 요청을 보냅니다.
    result = response.json()  # JSON 응답을 딕셔너리로 변환합니다.

    st.success(result["feedback"])  # 백엔드가 만든 피드백 문장을 화면에 표시합니다.
    st.json(result)  # 전체 JSON 응답도 함께 보여 주어 데이터 구조를 확인합니다.
