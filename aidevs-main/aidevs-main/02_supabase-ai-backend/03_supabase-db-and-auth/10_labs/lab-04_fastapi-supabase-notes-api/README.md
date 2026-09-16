# Lab 04 - FastAPI와 Supabase Notes API

이 실습은 FastAPI endpoint가 Supabase 테이블과 연결되는 흐름을 확인합니다.

## 학습 목표

- 브라우저 또는 Swagger UI에서 FastAPI endpoint를 호출할 수 있습니다.
- `/notes` API가 Supabase의 `learning_notes` 테이블과 연결되는 흐름을 설명할 수 있습니다.
- 백엔드 API와 데이터베이스의 역할을 구분할 수 있습니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

브라우저에서 Swagger UI를 엽니다.

```text
http://127.0.0.1:8000/docs
```

## 확인할 endpoint

- `GET /health`
- `GET /notes`
- `POST /notes`
- `PUT /notes/{note_id}`
- `DELETE /notes/{note_id}`

## 확인 기준

- Swagger UI에서 `POST /notes`로 새 데이터를 만들 수 있습니다.
- Supabase Table Editor에서 생성된 데이터가 보입니다.
- `GET /notes`로 방금 만든 데이터가 조회됩니다.
- 수정과 삭제 후 Supabase Table Editor의 데이터 상태가 달라집니다.
