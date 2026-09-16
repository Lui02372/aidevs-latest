# 12. Postman 선택 설치 가이드

Postman은 HTTP API를 테스트하는 도구입니다.

FastAPI는 Swagger UI(`/docs`)를 기본 제공하므로 Postman이 필수는 아닙니다. 다만 실제 API 테스트 도구를 경험하고 싶다면 선택적으로 사용합니다.

공식 사이트:

```text
https://www.postman.com/downloads/
```

## 1. 언제 사용하나요?

```text
FastAPI endpoint를 직접 호출할 때
GET/POST/PUT/DELETE 요청을 비교할 때
Authorization header를 넣어 테스트할 때
JSON body를 직접 작성해 요청할 때
```

## 2. 설치

브라우저에서 공식 다운로드 페이지로 이동합니다.

```text
https://www.postman.com/downloads/
```

Windows용 설치 파일을 다운로드해 설치합니다.

## 3. FastAPI 테스트 예시

FastAPI 서버 실행:

```powershell
uvicorn main:app --reload
```

Postman에서 요청:

```text
Method: GET
URL: http://127.0.0.1:8000/health
```

POST JSON 예시:

```json
{
  "message": "안녕하세요"
}
```

## 4. Swagger와 Postman 차이

| 항목 | Swagger UI | Postman |
| --- | --- | --- |
| 위치 | FastAPI `/docs` | 별도 프로그램 |
| 장점 | 설치 없이 바로 사용 | 요청 저장, header/body 관리 편리 |
| 추천 시점 | 초보자 첫 테스트 | 반복 API 테스트 |

## 5. 체크리스트

```text
[ ] Postman 설치 여부를 결정했다.
[ ] Swagger UI만으로도 기본 실습이 가능하다는 점을 이해했다.
[ ] Authorization header를 어디에 넣는지 확인했다.
```

