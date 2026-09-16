import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.

API_BASE_URL = "http://127.0.0.1:8000"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

health_url = f"{API_BASE_URL}/health"  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
courses_url = f"{API_BASE_URL}/api/courses"  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

health_response = httpx.get(health_url, timeout=5.0)  # 지정한 URL로 GET 요청을 보내 데이터를 조회합니다.
courses_response = httpx.get(courses_url, timeout=5.0)  # 지정한 URL로 GET 요청을 보내 데이터를 조회합니다.

print("health:", health_response.json())  # 터미널에 값을 출력해 코드 실행 결과를 확인합니다.
print("courses:", courses_response.json())  # 터미널에 값을 출력해 코드 실행 결과를 확인합니다.

