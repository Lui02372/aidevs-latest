# Postman 테스트

Postman은 API를 브라우저보다 자세히 테스트할 수 있는 도구입니다. 설치되어 있지 않다면 아래 순서로 준비합니다.

## Postman 설치

1. 브라우저에서 Postman 공식 다운로드 페이지를 엽니다.

```text
https://www.postman.com/downloads/
```

2. Windows용 설치 파일을 내려받아 실행합니다.
3. 설치가 끝나면 Postman을 실행합니다.
4. 로그인 화면이 나오면 계정으로 로그인하거나, 가능한 경우 가벼운 테스트용으로 계속 진행합니다.
5. 새 요청을 만들고 Method, URL, Body를 입력해 FastAPI API를 테스트합니다.

Postman 설치가 어렵다면 이 단원에서는 Swagger UI(`/docs`)와 PowerShell `Invoke-RestMethod`로도 같은 API 흐름을 확인할 수 있습니다.

## 먼저 실행할 예제

오류 처리 예제를 확인할 때는 아래 파일을 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
uvicorn 01_http-exception:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 01_http-exception:app --reload
```

## GET 요청

```text
GET http://127.0.0.1:8000/items/1
```

정상 응답 예시입니다.

```json
{
  "data": {
    "id": 1,
    "name": "Python 교재",
    "price": 18000
  }
}
```

없는 데이터를 조회하는 요청도 확인합니다.

```text
GET http://127.0.0.1:8000/items/999
```

이 요청은 404 응답을 확인하기 위한 예시입니다.

## 서비스 규칙 오류 요청

아래 요청은 존재하는 상품이지만 가격이 0원이므로 구매할 수 없다는 400 응답을 확인합니다.

```text
GET http://127.0.0.1:8000/items/2/buy
```

## POST 요청

POST Body를 확인할 때는 테스트용 앱을 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\05_error-handling-and-testing
uvicorn app_for_test:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app_for_test:app --reload
```

Postman에서 새 요청을 만들고 아래처럼 입력합니다.

```text
POST http://127.0.0.1:8000/messages
```

Body 탭에서 `raw`와 `JSON`을 선택합니다.

```json
{
  "text": "hello"
}
```

`text`를 빈 문자열로 보내면 Pydantic 검증에 의해 422 응답을 확인할 수 있습니다.

