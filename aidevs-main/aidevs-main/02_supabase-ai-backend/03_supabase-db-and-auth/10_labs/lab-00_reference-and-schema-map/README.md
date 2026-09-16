# Lab 00 - Reference And Schema Map

이 lab은 코드를 실행하기 전에 `03_supabase-db-and-auth`에서 어떤 참고 문서와 SQL 파일을 사용하는지 확인하는 준비 실습입니다.

## 학습 목표

- `00_references` 폴더의 역할을 설명할 수 있습니다.
- 공통 SQL 파일인 `supabase-schema.sql` 위치를 찾을 수 있습니다.
- 어떤 챕터에서 어떤 테이블을 사용하는지 연결할 수 있습니다.

## 확인할 파일

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\README.md
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\env-and-secret-management.md
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\auth-basic-guide.md
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\session-patterns.md
```

## 확인 기준

| 확인 항목 | 기준 |
|---|---|
| `learning_notes` | 02 CRUD, 03 FastAPI notes API에서 사용합니다. |
| `simple_chat_logs` | 05 대화 로그 저장 실습에서 사용합니다. |
| Supabase key 관리 | `.env`에 저장하고 GitHub에 올리지 않습니다. |
| JWT/Bearer token | 04 Auth 실습에서 사용합니다. |
| Redis TTL cache | 06 Upstash Redis 실습에서 사용합니다. |

## 정리 질문

- `00_references`는 왜 실습 코드 폴더와 분리되어 있나요?
- `learning_notes`와 `simple_chat_logs`는 각각 어느 챕터에서 사용하나요?
- `.env`와 `.env.example`에는 각각 어떤 값이 들어가야 하나요?
