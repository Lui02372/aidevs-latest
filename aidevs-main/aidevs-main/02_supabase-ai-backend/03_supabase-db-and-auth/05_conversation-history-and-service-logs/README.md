# 05. 대화 이력과 서비스 로그 저장

이 챕터에서는 AI 서비스에서 생성되는 사용자 질문, AI 답변, 실행 상태를 Supabase에 저장하는 흐름을 배웁니다.

처음부터 `conversations`, `messages`, `service_logs`처럼 테이블을 여러 개로 나누면 구조는 좋지만 초보자에게는 흐름이 복잡할 수 있습니다. 그래서 이 챕터는 먼저 `simple_chat_logs`라는 테이블 하나로 시작합니다.

## 학습 목표

- 사용자 질문과 AI 답변을 Supabase에 저장하는 이유를 이해합니다.
- FastAPI endpoint에서 LLM을 호출하고 결과를 DB에 남기는 흐름을 이해합니다.
- 성공 로그와 실패 로그를 같은 테이블에 남기는 방법을 확인합니다.
- 이후 복잡한 대화방/메시지/서비스 로그 구조로 확장할 수 있는 기준을 이해합니다.

## 전체 흐름

```text
사용자 질문
-> FastAPI endpoint
-> Gemini SDK 호출
-> AI 답변 생성
-> simple_chat_logs 테이블에 질문/답변/상태 저장
-> Swagger 또는 Supabase Table Editor에서 결과 확인
```

## simple_chat_logs 테이블

Supabase SQL Editor에서 아래 SQL을 실행합니다.

```sql
create table if not exists simple_chat_logs (
  id uuid primary key default gen_random_uuid(),
  user_message text not null,
  assistant_message text,
  provider text not null default 'gemini',
  model text,
  status text not null default 'success',
  error_message text,
  created_at timestamptz not null default now()
);
```

지금 단계에서는 인덱스를 만들지 않습니다. 데이터가 많아지고 `created_at`, `status` 기준 조회가 느려지는 시점에 성능 개선 내용으로 다시 다룹니다.

`simple_chat_logs`에는 `user_id`를 두지 않습니다. 이 테이블은 로그인 사용자 구분 없이 “질문과 답변을 DB에 저장한다”는 최소 흐름을 확인하기 위한 예제입니다. 사용자별 대화 이력은 Auth/JWT를 연결한 뒤 `conversations`, `messages`, `service_logs` 같은 확장 구조에서 다룹니다.

전체 스키마 파일에도 같은 내용이 포함되어 있습니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

## 컬럼 의미

| 컬럼 | 의미 |
| --- | --- |
| `id` | 로그 1건의 고유 id |
| `user_message` | 사용자가 입력한 질문 |
| `assistant_message` | AI가 생성한 답변 |
| `provider` | 사용한 LLM 제공자. 예: `gemini`, `mock` |
| `model` | 사용한 모델 이름 |
| `status` | 처리 결과. 예: `success`, `error` |
| `error_message` | 실패했을 때 오류 내용 |
| `created_at` | 로그가 저장된 시간 |

`user_id`가 없는 이유:

```text
현재 예제:
  로그인 사용자 구분 없이 질문/답변 저장 흐름만 확인합니다.

나중에 확장:
  Authorization: Bearer <access_token>
  -> 현재 사용자 확인
  -> user_id와 함께 대화 이력 저장
```

## 예제 01 - 단순 로그 저장

[01_insert_conversation_and_log.py](C:/aidev/02_supabase-ai-backend/03_supabase-db-and-auth/05_conversation-history-and-service-logs/01_insert_conversation_and_log.py)는 실제 LLM을 호출하지 않고, 샘플 질문/답변을 `simple_chat_logs`에 저장합니다.

실행:

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\05_conversation-history-and-service-logs\01_insert_conversation_and_log.py
```

이 예제에서 확인할 것:

```text
1. simple_chat_logs에 로그 1건이 저장됩니다.
2. provider는 mock으로 저장됩니다.
3. status는 success로 저장됩니다.
4. 최근 로그를 다시 조회합니다.
```

## 예제 02 - FastAPI + LLM + 로그 저장

[02_fastapi_llm_chat_log.py](C:/aidev/02_supabase-ai-backend/03_supabase-db-and-auth/05_conversation-history-and-service-logs/02_fastapi_llm_chat_log.py)는 Swagger에서 질문을 입력하면 Gemini SDK로 답변을 만들고, 질문과 답변을 `simple_chat_logs`에 저장합니다.

실행:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_llm_chat_log:app --reload --host 127.0.0.1 --port 8003
```

Swagger 주소:

```text
http://127.0.0.1:8003/docs
```

Swagger에서 확인할 endpoint:

| Endpoint | Method | 역할 |
| --- | --- | --- |
| `/health` | GET | FastAPI 서버 실행 확인 |
| `/chat` | POST | Gemini에 질문하고 로그 저장 |
| `/logs` | GET | 최근 채팅 로그 조회 |

## 실행 전 준비

`.env` 파일에 아래 값이 필요합니다.

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

`01_insert_conversation_and_log.py`는 Gemini를 호출하지 않으므로 `GEMINI_API_KEY`가 없어도 됩니다. `02_fastapi_llm_chat_log.py`는 실제 Gemini를 호출하므로 `GEMINI_API_KEY`가 필요합니다.

## 자주 만나는 문제

### Could not find the table simple_chat_logs

Supabase에 `simple_chat_logs` 테이블이 아직 만들어지지 않은 상태입니다.

해결 방법:

1. Supabase Dashboard의 SQL Editor를 엽니다.
2. 이 README의 `simple_chat_logs` SQL 또는 `00_references/supabase-schema.sql` 내용을 실행합니다.
3. Table Editor에서 `simple_chat_logs` 테이블이 보이는지 확인합니다.
4. 예제를 다시 실행합니다.

### GEMINI_API_KEY 오류가 나는 경우

`02_fastapi_llm_chat_log.py`는 실제 Gemini API를 호출합니다. `.env`에 실제 `GEMINI_API_KEY`가 들어 있는지 확인합니다.

### Gemini 503 또는 quota 오류가 나는 경우

Gemini 서버가 일시적으로 바쁘거나 호출 제한에 걸린 상태일 수 있습니다. 잠시 뒤 다시 실행하거나 `.env`의 `GEMINI_MODEL` 값을 다른 사용 가능한 모델로 바꿔 봅니다.

### 로그 저장은 됐는데 답변이 비어 있는 경우

Gemini 응답이 비어 있거나 오류가 발생했을 수 있습니다. Supabase Table Editor에서 `status`, `error_message` 컬럼을 확인합니다.

## 다음 단계

`simple_chat_logs`는 수업 초반에 흐름을 이해하기 위한 단순 구조입니다. 실제 서비스에서는 이후 아래처럼 테이블을 나누어 확장할 수 있습니다.

| 확장 테이블 | 역할 |
| --- | --- |
| `conversations` | 대화방 또는 대화 세션 |
| `messages` | 대화방 안의 사용자/AI 메시지 |
| `service_logs` | API 호출, 오류, 처리 시간 같은 운영 로그 |

즉, 이 챕터에서는 먼저 한 테이블로 흐름을 이해하고, 나중에 미니 프로젝트에서 더 정교한 구조로 확장합니다.

## 완료 체크리스트

```text
[ ] simple_chat_logs 테이블을 만들었습니다.
[ ] 01 예제로 샘플 로그를 저장했습니다.
[ ] 02 예제로 Swagger에서 LLM 질문/답변을 실행했습니다.
[ ] Supabase Table Editor에서 user_message와 assistant_message를 확인했습니다.
[ ] status와 error_message 컬럼의 의미를 설명할 수 있습니다.
```
