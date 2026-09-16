# 03. 데이터베이스 설계서 샘플

프로젝트명: AI 서비스 로그 분석 및 운영 대시보드 구축

## 테이블 목록

| 테이블 | 역할 |
| --- | --- |
| `realtime_service_logs` | AI 서비스 요청, 응답, 오류, 성능 로그 저장 |
| `ai_answer_feedback` | AI 답변 품질 개선을 위한 사용자 피드백 저장 |

## 논리 ERD

```text
realtime_service_logs
  1 ─── 0..N ai_answer_feedback
```

하나의 서비스 로그에는 여러 피드백이 연결될 수 있습니다. 피드백은 특정 로그 없이도 저장할 수 있도록 `log_id`를 nullable로 둘 수 있습니다.

## 물리 ERD

### realtime_service_logs

| 컬럼 | 타입 | 제약조건 | 설명 |
| --- | --- | --- | --- |
| `id` | uuid | PK, default `gen_random_uuid()` | 로그 식별자 |
| `level` | text | NOT NULL, default `info` | info/warning/error |
| `source` | text | NOT NULL, default `backend` | 로그 발생 위치 |
| `message` | text | NOT NULL | 로그 메시지 |
| `request_path` | text | nullable | API 경로 |
| `status_code` | integer | nullable | HTTP 상태 코드 |
| `latency_ms` | integer | nullable | 응답 시간 |
| `metadata` | jsonb | NOT NULL, default `{}` | 추가 정보 |
| `created_at` | timestamptz | NOT NULL, default `now()` | 생성 시각 |

### ai_answer_feedback

| 컬럼 | 타입 | 제약조건 | 설명 |
| --- | --- | --- | --- |
| `id` | uuid | PK, default `gen_random_uuid()` | 피드백 식별자 |
| `log_id` | uuid | FK, nullable | 연결된 서비스 로그 |
| `rating` | integer | CHECK 1~5 | 사용자 평가 점수 |
| `comment` | text | nullable | 사용자 의견 |
| `improvement_note` | text | nullable | 개선 메모 |
| `created_at` | timestamptz | NOT NULL, default `now()` | 생성 시각 |

## 3NF 점검

- [ ] 각 테이블은 하나의 주제만 가진다.
- [ ] 반복되는 그룹이 없다.
- [ ] 일반 컬럼은 기본키에만 종속된다.
- [ ] 로그와 피드백은 별도 테이블로 분리되어 데이터 중복을 줄인다.

## 체크리스트

- [ ] 테이블이 3정규화 기준으로 설계되었다.
- [ ] 데이터 중복이 최소화되었다.
- [ ] 삽입/갱신/삭제 이상현상을 줄일 수 있다.
- [ ] 논리 ERD와 물리 ERD가 모두 작성되었다.
- [ ] 테이블명, 컬럼, PK/FK가 명확하다.
- [ ] 모든 컬럼의 데이터 타입, 제약조건, 기본값, 코멘트가 정의되었다.
