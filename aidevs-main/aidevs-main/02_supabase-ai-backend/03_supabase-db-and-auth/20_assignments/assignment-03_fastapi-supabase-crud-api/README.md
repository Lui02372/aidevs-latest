# Assignment 03 - FastAPI와 Supabase CRUD API

FastAPI endpoint를 만들고 Supabase 테이블과 연결하는 과제입니다.

## 목표

- HTTP Method와 CRUD 동작을 연결할 수 있습니다.
- Swagger UI에서 API를 테스트할 수 있습니다.
- API 호출 결과가 Supabase 테이블에 반영되는지 확인할 수 있습니다.

## 제출물

아래 내용을 포함해 작성합니다.

```text
1. 구현한 endpoint 목록
2. 각 endpoint의 HTTP Method
3. Request Body 예시
4. Response 예시
5. Swagger UI 테스트 결과
6. Supabase Table Editor 확인 결과
7. 오류 발생 시 해결 과정
```

## 필수 endpoint

```text
GET /health
GET /notes
POST /notes
PUT /notes/{note_id}
DELETE /notes/{note_id}
```

## 실행 참고

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

## 확인 기준

- `POST /notes`로 데이터를 생성할 수 있습니다.
- `GET /notes`로 생성한 데이터를 조회할 수 있습니다.
- `PUT`, `DELETE` 결과가 Supabase에 반영됩니다.
- 오류 응답이 이해 가능한 메시지를 반환합니다.
