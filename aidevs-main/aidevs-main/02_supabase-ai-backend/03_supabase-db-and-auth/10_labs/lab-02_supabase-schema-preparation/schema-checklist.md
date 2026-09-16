# Schema Checklist

Supabase SQL Editor에서 `supabase-schema.sql`을 실행한 뒤 아래 항목을 확인합니다.

## 필수 테이블

| 확인 | 항목 |
|---|---|
| [ ] | `learning_notes` 테이블이 있습니다. |
| [ ] | `learning_notes.id`가 `uuid` 기본키입니다. |
| [ ] | `learning_notes.title`과 `learning_notes.content`가 있습니다. |
| [ ] | `simple_chat_logs` 테이블이 있습니다. |
| [ ] | `simple_chat_logs.user_message`가 있습니다. |
| [ ] | `simple_chat_logs.assistant_message`가 있습니다. |
| [ ] | `simple_chat_logs.status`와 `simple_chat_logs.error_message`가 있습니다. |

## 참고 테이블

| 확인 | 항목 |
|---|---|
| [ ] | `conversations` 테이블이 있습니다. |
| [ ] | `messages` 테이블이 있습니다. |
| [ ] | `service_logs` 테이블이 있습니다. |

## 보안 확인

| 확인 | 항목 |
|---|---|
| [ ] | SQL 파일에 실제 API key가 들어 있지 않습니다. |
| [ ] | `.env` 파일은 GitHub에 올리지 않습니다. |
| [ ] | `SUPABASE_SERVICE_ROLE_KEY`는 서버 코드에서만 사용합니다. |

## 오류가 날 때

`PGRST205`, `Could not find the table` 오류가 나오면 테이블이 없거나 Supabase API schema cache가 아직 갱신되지 않은 상태일 수 있습니다.

먼저 SQL Editor에서 테이블이 생성되었는지 확인하고, 잠시 기다린 뒤 코드를 다시 실행합니다.
