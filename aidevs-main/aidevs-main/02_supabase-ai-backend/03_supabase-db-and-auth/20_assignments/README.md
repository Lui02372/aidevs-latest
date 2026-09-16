# 20_assignments

이 폴더는 `03_supabase-db-and-auth`의 `00`부터 `06`까지 배운 내용을 바탕으로 작성하는 제출 과제 공간입니다.

`10_labs`가 함께 따라 하며 실행 결과를 확인하는 실습이라면, `20_assignments`는 학습 내용을 바탕으로 스스로 정리하고 설계하는 과제입니다.

## 과제 기준

현재 과제는 아래 범위까지만 필수로 다룹니다.

```text
00_references
01_supabase-project-and-env
02_supabase-table-and-crud
03_fastapi-supabase-integration
04_supabase-auth-and-rls
05_conversation-history-and-service-logs
06_upstash-redis-cache-and-session
```

이번 범위에서 RLS 정책 SQL 작성, Redis rate limit 구현, Redis session/cache-aside 구현은 필수가 아닙니다.

## 과제 목록

| 순서 | 폴더 | 주제 | 핵심 제출물 |
|---|---|---|---|
| 0 | `assignment-00_reference-schema-map` | 참고 문서와 스키마 구조 파악 | 문서/테이블 연결표 |
| 1 | `assignment-01_supabase-project-env-report` | Supabase 프로젝트와 환경변수 준비 | 환경 준비 보고서 |
| 2 | `assignment-02_schema-design-and-sql` | 필수 테이블 구조 확인 | `learning_notes`, `simple_chat_logs` 설명 |
| 3 | `assignment-03_fastapi-supabase-crud-api` | FastAPI와 Supabase CRUD API | API 설계 문서, 실행 결과 |
| 4 | `assignment-04_auth-jwt-bearer-flow` | Auth/JWT/Bearer token 흐름 | 인증 흐름 설명서 |
| 5 | `assignment-05_conversation-service-log-design` | `simple_chat_logs` 기반 대화 로그 저장 | 저장 흐름 설계서 |
| 6 | `assignment-06_upstash-redis-ttl-cache` | Upstash Redis TTL 캐시 | Redis 캐시 사용 설계서 |
| 7 | `assignment-07_integrated-db-auth-cache-plan` | Supabase + Auth + Redis 통합 설계 | 통합 아키텍처 문서 |
| 99 | `assignment-99_supabase-db-auth-mini-design` | 최종 미니 설계 과제 | 미니 프로젝트 설계서 |

## 공통 제출 형식

과제 제출 문서는 Markdown 형식으로 작성합니다.

```text
제목
목표
구현 또는 설계 내용
실행 방법
실행 결과
오류와 해결 과정
정리한 내용
```

환경변수와 API key는 절대 문서에 그대로 적지 않습니다.

잘못된 예:

```text
SUPABASE_SERVICE_ROLE_KEY=실제-service-role-key-값
```

올바른 예:

```text
SUPABASE_SERVICE_ROLE_KEY=설정 완료, 실제 값은 제출하지 않음
```

## 공통 평가 기준

- `00_references`의 문서와 실제 실습 챕터를 연결해서 설명했는가?
- Supabase에 저장할 데이터와 Redis에 잠깐 저장할 데이터를 구분했는가?
- `anon key`와 `service role key`의 사용 위치를 올바르게 설명했는가?
- FastAPI endpoint의 URL, HTTP Method, Request/Response 구조가 명확한가?
- JWT와 Bearer token 흐름을 설명할 수 있는가?
- `simple_chat_logs`에 질문/답변/상태를 저장하는 이유를 설명했는가?
- Redis TTL과 캐시를 AI 서비스 비용과 응답 속도 관점에서 설명했는가?
- 오류 발생 시 원인과 해결 과정을 기록했는가?

## 과제 진행 전 확인

아래 명령으로 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Supabase 테이블이 없다면 아래 SQL 파일을 Supabase SQL Editor에서 실행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

## 제출 전 최종 점검

- 실제 API key를 문서나 GitHub에 올리지 않았습니다.
- `.env` 파일을 제출하지 않았습니다.
- 실행 화면 또는 터미널 결과를 캡처하거나 텍스트로 정리했습니다.
- Supabase Table Editor에서 데이터 저장 결과를 확인했습니다.
- Upstash Redis를 사용한 경우 TTL 또는 캐시 재사용 결과를 확인했습니다.
- 오류가 발생했다면 오류 메시지와 해결 과정을 함께 기록했습니다.
