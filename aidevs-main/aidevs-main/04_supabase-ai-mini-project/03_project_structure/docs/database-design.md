# Database Design

이 문서는 팀 프로젝트의 데이터베이스 설계서 starter입니다.

`database/schema.sql`과 `02_project-deliverables/03_database-design-sample.md`를 함께 참고하세요.

## 작성할 내용

- 테이블 목록
- 컬럼 정의
- PK/FK 관계
- 제약조건
- 데이터 예시
- API와 연결되는 테이블

## 테이블 예시

### realtime_service_logs

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `uuid` | 로그 고유 ID |
| `level` | `text` | 로그 수준 |
| `source` | `text` | 로그 발생 위치 |
| `message` | `text` | 로그 메시지 |
| `request_path` | `text` | 요청 경로 |
| `status_code` | `integer` | HTTP 상태 코드 |
| `latency_ms` | `integer` | 처리 시간 |
| `metadata` | `jsonb` | 추가 정보 |
| `created_at` | `timestamptz` | 생성 시각 |

### ai_answer_feedback

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `uuid` | 피드백 고유 ID |
| `log_id` | `uuid` | 연결된 로그 ID |
| `rating` | `integer` | 1~5점 |
| `comment` | `text` | 사용자 의견 |
| `improvement_note` | `text` | 개선 메모 |
| `created_at` | `timestamptz` | 생성 시각 |
