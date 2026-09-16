# API Design

이 문서는 팀 프로젝트의 API 설계서 starter입니다.

`02_project-deliverables/01_api-design-sample.md`를 참고해 실제 구현 내용으로 수정하세요.

## 작성할 내용

- API 목적
- endpoint 목록
- HTTP Method
- Request/Response Pydantic 모델
- 표준 에러 응답 형식
- 인증 또는 환경 변수 사용 여부

## Endpoint 예시

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 상태 확인 |
| POST | `/logs` | 서비스 로그 생성 |
| GET | `/logs` | 최근 서비스 로그 조회 |
| GET | `/logs/summary` | 로그 통계 요약 |
| GET | `/stream/logs` | SSE 기반 실시간 로그 스트림 |
| POST | `/feedback` | AI 답변 피드백 저장 |

## 에러 응답 예시

```json
{
  "error_code": "LOG_CREATE_FAILED",
  "message": "로그 저장에 실패했습니다.",
  "detail": "Supabase 연결 정보를 확인하세요."
}
```
