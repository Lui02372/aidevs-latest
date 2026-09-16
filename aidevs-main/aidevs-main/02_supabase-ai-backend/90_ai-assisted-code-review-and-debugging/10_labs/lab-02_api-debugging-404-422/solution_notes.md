# Lab 02 Solution Notes

## 오류 구분

| 상황 | 상태 코드 | 이유 |
|---|---|---|
| `POST /ai/missing` | 404 | 해당 URL의 endpoint가 없습니다. |
| 브라우저 주소창에서 `/ai/chat` 접속 | 405 | `/ai/chat`은 POST endpoint인데 브라우저 주소창은 GET으로 호출합니다. |
| `{"message": ""}` | 422 | `min_length=1` 조건을 통과하지 못합니다. |
| `{"text": "hello"}` | 422 | Pydantic 모델은 `message` 필드를 요구합니다. |

## 확인 방법

Swagger에서 `POST /ai/chat`을 열고 아래 Body로 실행합니다.

```json
{
  "message": "FastAPI 오류를 설명해줘"
}
```

## 좋은 프롬프트 포인트

URL, Method, 요청 Body, 응답 JSON을 함께 전달해야 원인을 빠르게 좁힐 수 있습니다.
