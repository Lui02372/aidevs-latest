# 05_error-handling-and-testing

예외 처리, 의존성 주입, 미들웨어, CORS, API 테스트 기초를 학습합니다.

API는 정상 응답만큼 오류 응답도 중요합니다. 이 챕터에서는 클라이언트가 이해할 수 있는 오류 메시지와 상태 코드를 반환하는 방법을 학습합니다.

FastAPI에서는 여러 API에서 반복되는 공통 로직을 `Depends`로 분리할 수 있습니다. 예를 들어 사용자 인증, 권한 확인, 설정값 확인, 데이터베이스 연결 준비 같은 작업은 각 엔드포인트 안에 계속 복사하기보다 의존성 함수로 분리하는 것이 좋습니다.

## 예제 파일

```text
01_http-exception.py
02_middleware-cors.py
03_swagger-test-guide.md
04_postman-test-guide.md
05_simple-test-client.py
app_for_test.py
dependency_injection_depends.py
global_exception_handler.py
```

## 확인할 것

- 없는 데이터를 요청했을 때 404가 반환되는가?
- 잘못된 요청 조건에서 400이 반환되는가?
- CORS 허용 origin을 코드에서 확인할 수 있는가?
- TestClient로 `/health`, `/messages`를 코드에서 호출할 수 있는가?
- `Depends`를 통해 현재 사용자 정보를 공통으로 가져올 수 있는가?
- 전역 예외 처리기가 오류 응답 형식을 일관되게 만들어 주는가?

## 핵심 개념

| 개념 | 의미 | 수업 예시 |
| --- | --- | --- |
| `HTTPException` | 특정 상황에서 의도적으로 HTTP 오류를 반환합니다. | 없는 상품을 요청하면 404를 반환합니다. |
| `Depends` | 여러 API에서 반복되는 공통 로직을 함수로 분리합니다. | 토큰을 확인하고 현재 사용자 정보를 가져옵니다. |
| Exception Handler | 예상한 오류를 같은 형식의 JSON 응답으로 바꿉니다. | 비즈니스 오류를 `error_code`, `message` 형태로 반환합니다. |
| Middleware | 모든 요청과 응답 사이에 공통 처리를 끼워 넣습니다. | 요청 처리 시간을 헤더에 추가합니다. |
| CORS | 브라우저가 다른 주소의 API를 호출할 수 있도록 허용합니다. | Streamlit 또는 프론트엔드 화면에서 FastAPI를 호출합니다. |

## 자주 보는 HTTP 상태 코드

| 상태 코드 | 이름 | 의미 | 이 단원에서 확인하는 예 |
| --- | --- | --- | --- |
| 200 | OK | 요청이 정상 처리되었습니다. | `/health`, `/items/1` 조회 성공 |
| 201 | Created | 새 데이터가 생성되었습니다. | 이후 POST 생성 API에서 사용 |
| 400 | Bad Request | 요청 조건이 잘못되었습니다. | 무료 상품 구매 요청처럼 서비스 규칙에 맞지 않는 요청 |
| 404 | Not Found | 요청한 데이터를 찾을 수 없습니다. | `/items/999`처럼 없는 id 조회 |
| 422 | Unprocessable Entity | 요청 JSON이 Pydantic 모델의 검증 조건과 맞지 않습니다. | 필수 필드 누락, 빈 문자열, 잘못된 타입 |
| 500 | Internal Server Error | 서버 내부에서 예상하지 못한 오류가 발생했습니다. | 처리하지 못한 예외 |

## 수업 진행 팁

1. 먼저 `01_http-exception.py`로 404, 400 오류를 확인합니다.
2. `dependency_injection_depends.py`로 인증 공통 로직을 분리하는 이유를 설명합니다.
3. `global_exception_handler.py`로 오류 응답 형식을 통일하는 방법을 확인합니다.
4. `02_middleware-cors.py`로 프론트엔드와 백엔드 주소가 다를 때 CORS가 왜 필요한지 설명합니다.

