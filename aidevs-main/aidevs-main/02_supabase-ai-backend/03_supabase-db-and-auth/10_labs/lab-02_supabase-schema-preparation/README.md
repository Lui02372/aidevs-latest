# Lab 02 - Supabase Schema Preparation

이 lab은 Python/FastAPI 코드를 실행하기 전에 Supabase 테이블을 준비하는 실습입니다.

현재 `00`~`06` 흐름에서 필수로 확인할 테이블은 `learning_notes`와 `simple_chat_logs`입니다.

## 학습 목표

- Supabase SQL Editor에서 SQL 파일을 실행할 수 있습니다.
- `learning_notes`와 `simple_chat_logs`가 어떤 실습에서 사용되는지 설명할 수 있습니다.
- 테이블이 없을 때 발생하는 오류를 코드 오류와 구분할 수 있습니다.

## 진행 방법

1. Supabase Dashboard에 접속합니다.
2. 실습 프로젝트를 선택합니다.
3. 왼쪽 메뉴에서 `SQL Editor`를 엽니다.
4. 아래 파일 내용을 복사해서 실행합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

## 필수 확인 테이블

| 테이블 | 사용 위치 | 확인 기준 |
|---|---|---|
| `learning_notes` | 02 CRUD, 03 FastAPI notes API | `id`, `title`, `content`, `created_at` 컬럼이 있습니다. |
| `simple_chat_logs` | 05 대화 로그 저장 | `user_message`, `assistant_message`, `provider`, `model`, `status`, `error_message`, `created_at` 컬럼이 있습니다. |

## 참고 확인 테이블

| 테이블 | 의미 |
|---|---|
| `conversations` | 이후 사용자별 대화방 구조로 확장할 때 사용합니다. |
| `messages` | 이후 대화방 안의 사용자/AI 메시지를 나눠 저장할 때 사용합니다. |
| `service_logs` | 이후 API 호출 로그를 별도 테이블로 분리할 때 사용합니다. |

현재 lab에서는 참고 테이블을 직접 사용하는 코드까지 실행하지 않습니다.

## 체크리스트

자세한 확인 항목은 같은 폴더의 `schema-checklist.md`를 사용합니다.
