import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.

API_URL = "http://127.0.0.1:8000/api/message"  # 메시지를 전송할 POST API 주소입니다.
payload = {"name": "Kim", "message": "Streamlit에서 보낼 메시지입니다."}  # 백엔드에 JSON 본문으로 보낼 데이터입니다.

response = httpx.post(API_URL, json=payload, timeout=5.0)  # POST 요청을 보내고 응답 객체를 response 변수에 저장합니다.

print("status code:", response.status_code)  # HTTP 요청이 성공했는지 확인할 수 있는 상태 코드를 출력합니다.
print("json:", response.json())  # 백엔드가 반환한 JSON 응답을 딕셔너리 형태로 출력합니다.

result = response.json()
print(result["name"])
print(result["message"])