# 01. API 설계 문서 샘플

프로젝트명: AI 서비스 로그 분석 및 운영 대시보드 구축

## API 설계 원칙

- URL은 리소스 중심으로 명명합니다.
- HTTP Method는 의미에 맞게 사용합니다.
- 오류 응답은 공통 형식을 따릅니다.
- Request/Response 모델은 Pydantic 기준으로 정의합니다.

## Endpoint 목록

| Method | URL | 설명 | Request | Response |
| --- | --- | --- | --- | --- |
| GET | `/health` | 백엔드 상태 확인 | 없음 | 상태 정보 |
| POST | `/logs` | 서비스 로그 생성 | `LogCreate` | `LogItem` |
| GET | `/logs` | 최근 서비스 로그 조회 | query: `limit` | `list[LogItem]` |
| GET | `/logs/summary` | level별 로그 수 조회 | 없음 | `list[LogSummary]` |
| GET | `/stream/logs` | SSE 실시간 로그 스트림 | 없음 | `text/event-stream` |
| POST | `/feedback` | AI 답변 피드백 저장 | `FeedbackCreate` | `FeedbackItem` |
| GET | `/feedback` | 피드백 목록 조회 | 없음 | `list[FeedbackItem]` |

## 표준 에러 응답

```json
{
  "status_code": 400,
  "error_code": "INVALID_REQUEST",
  "message": "요청 데이터가 올바르지 않습니다.",
  "detail": {
    "field": "message",
    "reason": "message는 비어 있을 수 없습니다."
  }
}
```

## 예외 처리 규칙

| 상황 | HTTP Status | error_code | 처리 |
| --- | --- | --- | --- |
| 요청 필드 누락 | 422 | `VALIDATION_ERROR` | FastAPI/Pydantic 검증 오류를 사용자 메시지로 표시 |
| 로그를 찾을 수 없음 | 404 | `LOG_NOT_FOUND` | 상세 조회 시 안내 메시지 반환 |
| Supabase 연결 실패 | 500 | `DATABASE_ERROR` | backend 로그 기록 후 오류 응답 |
| Redis 연결 실패 | 503 | `REDIS_UNAVAILABLE` | 메모리 fallback 또는 재시도 안내 |
| SSE 연결 실패 | 503 | `STREAM_ERROR` | 프론트엔드에서 재연결 안내 |

## Pydantic 모델 예시

```python
class LogCreate(BaseModel):
    level: str = Field(default="info", examples=["info"])
    source: str = Field(default="chat-api", examples=["chat-api"])
    message: str = Field(min_length=1, examples=["AI 응답 생성 완료"])
    request_path: str | None = Field(default="/chat")
    status_code: int | None = Field(default=200)
    latency_ms: int | None = Field(default=120)
    metadata: dict = Field(default_factory=dict)
```

## 체크리스트

- [ ] 엔드포인트 URL이 리소스 중심으로 일관되게 명명되었다.
- [ ] HTTP Method가 GET/POST/PUT/DELETE 의미에 맞게 사용되었다.
- [ ] 표준화된 에러 응답 포맷이 정의되었다.
- [ ] 4xx/5xx 예외 상황별 처리 규칙이 문서화되었다.
- [ ] Request/Response용 Pydantic 모델이 필수/선택 필드를 명확히 정의한다.
- [ ] 타입 힌트와 예시값이 포함되어 있다.
- [ ] 중첩 JSON은 nested 모델 또는 명확한 dict 구조로 표현된다.
