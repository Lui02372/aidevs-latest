# 03. FastAPI와 Supabase 연동

이 챕터에서는 FastAPI endpoint에서 Supabase 테이블을 호출하는 API 서버를 만듭니다.

앞 챕터에서 Python 파일을 직접 실행해 `learning_notes` CRUD를 확인했다면, 이번에는 같은 기능을 HTTP API로 제공합니다. 즉, 브라우저나 프론트엔드가 FastAPI에 요청을 보내고, FastAPI가 Supabase에 데이터를 저장하거나 조회하는 구조입니다.

## 학습 목표

- FastAPI endpoint에서 Supabase client를 사용합니다.
- Pydantic 모델로 요청 데이터를 검증합니다.
- `/health`로 서버와 환경 변수 상태를 확인합니다.
- `/notes` API로 Supabase 테이블 데이터를 생성/조회/수정/삭제합니다.
- update/delete에서 `id` 조건이 왜 중요한지 이해합니다.
- 이후 Streamlit 또는 프론트엔드에서 호출할 백엔드 API 구조를 이해합니다.

## 전체 흐름

```text
사용자 또는 Swagger UI
-> FastAPI endpoint
-> Pydantic 요청 검증
-> Supabase client
-> learning_notes 테이블
-> JSON 응답 반환
```

이 과정에서는 Docker PostgreSQL을 사용하지 않습니다. 데이터베이스는 Supabase managed PostgreSQL을 사용합니다.

## 실행 전 준비

### 1. Supabase 환경 변수 확인

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
dir .env
```

VS Code에서 `.env`를 열고 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`가 실제 값인지 확인합니다. key 전체 값은 터미널이나 문서에 출력하지 않습니다.

### 2. `learning_notes` 테이블 확인

Supabase SQL Editor에서 아래 SQL이 실행되어 있어야 합니다.

```sql
create table if not exists learning_notes_main (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text not null,
  created_at timestamp not null default now()
);
```

이미 `02_supabase-table-and-crud`를 완료했다면 이 테이블은 준비되어 있습니다.

## 서버 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 제공 endpoint

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | 서버와 Supabase 환경 변수 상태를 확인합니다. |
| GET | `/notes` | 최근 학습 메모 목록을 조회합니다. |
| GET | `/notes/{note_id}` | 학습 메모 1개를 id로 조회합니다. |
| POST | `/notes` | 새 학습 메모를 저장합니다. |
| PUT | `/notes/{note_id}` | 기존 학습 메모의 title/content를 수정합니다. |
| DELETE | `/notes/{note_id}` | 학습 메모를 삭제합니다. |

## Swagger UI 테스트 순서

### 1. 서버 상태 확인

`GET /health`를 실행합니다.

정상 예시:

```json
{
  "status": "ok",
  "database": "supabase",
  "supabase_url_configured": true,
  "service_role_key_configured": true
}
```

### 2. 메모 생성

`POST /notes`를 실행합니다.

요청 예시:

```json
{
  "title": "FastAPI Supabase integration",
  "content": "FastAPI endpoint에서 Supabase learning_notes 테이블에 데이터를 저장합니다."
}
```

응답에 들어 있는 `id`를 복사해 둡니다.

### 3. 메모 목록 조회

`GET /notes`를 실행합니다.

방금 만든 메모가 목록에 보이는지 확인합니다.

### 4. 메모 단건 조회

`GET /notes/{note_id}`를 실행합니다.

`note_id`에는 `POST /notes` 응답에서 받은 `id`를 넣습니다.

### 5. 메모 수정

`PUT /notes/{note_id}`를 실행합니다.

요청 예시:

```json
{
  "title": "FastAPI Supabase integration - updated",
  "content": "수정 API를 통해 title과 content를 변경했습니다."
}
```

### 6. 메모 삭제

`DELETE /notes/{note_id}`를 실행합니다.

삭제 후 `GET /notes/{note_id}`를 다시 실행하면 404 응답이 나와야 합니다.

## service role key 주의

이 예제는 백엔드 서버 코드입니다. 따라서 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.

```text
service role key는 강한 권한을 가진 서버용 key입니다.
브라우저, Streamlit 화면, GitHub 저장소에 노출하면 안 됩니다.
```

프론트엔드에서 직접 Supabase를 사용할 때는 anon key와 RLS 정책을 함께 사용합니다. 이 내용은 `04_supabase-auth-and-rls`에서 다룹니다.

## 자주 만나는 문제

### 500 Supabase environment values are missing

`.env`에 `SUPABASE_URL` 또는 `SUPABASE_SERVICE_ROLE_KEY`가 없거나 예시 값으로 남아 있을 수 있습니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
dir .env
```

`.env` 파일을 열어 `SUPABASE_URL`과 `SUPABASE_SERVICE_ROLE_KEY`가 실제 값인지 확인합니다.

### relation learning_notes does not exist

Supabase SQL Editor에서 `learning_notes` 테이블 생성 SQL을 먼저 실행해야 합니다.

### 404 Note not found

조회, 수정, 삭제하려는 `note_id`가 실제 테이블에 없을 때 발생합니다. `GET /notes`로 현재 존재하는 id를 먼저 확인합니다.

## 완료 체크리스트

```text
[ ] .env에 Supabase 값이 설정되어 있습니다.
[ ] learning_notes 테이블이 생성되어 있습니다.
[ ] uvicorn으로 FastAPI 서버를 실행했습니다.
[ ] Swagger UI에서 GET /health를 확인했습니다.
[ ] POST /notes로 메모를 생성했습니다.
[ ] GET /notes/{note_id}로 단건 조회를 확인했습니다.
[ ] PUT /notes/{note_id}로 수정했습니다.
[ ] DELETE /notes/{note_id}로 삭제했습니다.
[ ] Supabase Table Editor에서 데이터 흐름을 확인했습니다.
```
