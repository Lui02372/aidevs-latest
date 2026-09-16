# services

이 폴더에는 외부 시스템과 연결되는 로직을 추가합니다.

구현할 파일 예시:

```text
db_service.py
redis_service.py
sse_service.py
feedback_service.py
```

역할 예시:

```text
db_service.py
- Supabase DB에 로그 저장
- 최근 로그 조회
- level별 요약 조회

redis_service.py
- 새 로그 이벤트 publish
- 실시간 이벤트 subscribe

sse_service.py
- Upstash Redis 이벤트를 SSE 형식으로 변환

feedback_service.py
- AI 답변 품질 피드백 저장
- 피드백 목록 조회
```

프론트엔드가 Supabase나 Redis에 직접 연결하지 않도록 backend service 계층에서 처리합니다.
