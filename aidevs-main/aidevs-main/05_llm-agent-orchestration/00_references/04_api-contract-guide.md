# API 계약 가이드

## 구현 순서

```text
요청 JSON
→ 응답 JSON
→ Pydantic Schema
→ Mock Endpoint
→ Streamlit 연결
→ 실제 Agent 연결
```

## 공통 응답

```json
{
  "success": true,
  "data": {},
  "error": null,
  "trace_id": "trace-001"
}
```

## 현재 FastAPI 오류 응답

```json
{"detail": "출발 날짜를 확인해 주세요."}
```

성공 응답은 `ApiResponse`를 사용하고, 현재 오류는 FastAPI
`HTTPException`의 `detail` 형식을 사용합니다. Frontend의 `api_client.py`가
`detail`을 사용자가 이해할 수 있는 문장으로 변환합니다.

성공·오류를 완전히 같은 Envelope로 통일하는 작업은 후속 리팩터링 항목이며,
현재 구현에 존재하지 않는 `error.code`를 가정하지 않습니다.
