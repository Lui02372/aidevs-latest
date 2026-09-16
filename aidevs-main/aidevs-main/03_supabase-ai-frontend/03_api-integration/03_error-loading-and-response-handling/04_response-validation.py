import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.
import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

st.title("응답 데이터 검증")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

if st.button("과정 목록 검증"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    response = httpx.get(f"{API_BASE_URL}/api/courses", timeout=5.0)  # GET 요청의 응답을 response 변수에 저장해 상태 코드와 JSON 데이터를 확인합니다.
   
    data = response.json()  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

    if "courses" not in data:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.error("응답에 courses 항목이 없습니다.")  # 오류 상황을 사용자에게 명확히 보여줍니다.
    elif not isinstance(data["courses"], list):  # 앞 조건이 False일 때 추가 조건을 검사합니다.
        st.error("courses 항목은 리스트여야 합니다.")  # 오류 상황을 사용자에게 명확히 보여줍니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.success("응답 구조가 정상입니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
        st.write(data["courses"])  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

