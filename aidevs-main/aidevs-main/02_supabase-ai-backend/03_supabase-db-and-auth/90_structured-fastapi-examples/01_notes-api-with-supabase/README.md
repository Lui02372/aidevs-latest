# 01. Notes API With Supabase

Supabase에 노트를 저장하는 작은 CRUD 미니 프로젝트입니다. 폴더 이름과 `ex90_notes` 테이블은 그대로 유지합니다.

이 예제의 목표는 기능을 많이 만드는 것이 아니라, 요청이 어디를 거쳐 DB까지 가는지 한 번에 이해하는 것입니다.

```text
Swagger 또는 화면
      ↓ HTTP 요청
router (URL과 요청/응답)
      ↓
service (Supabase CRUD)
      ↓
Supabase ex90_notes 테이블
```

## 폴더별 역할

```text
01_notes-api-with-supabase
├─ app
│  ├─ main.py                 # FastAPI 앱을 만들고 router/예외 처리를 연결
│  ├─ core
│  │  ├─ config.py            # .env 읽기
│  ├─ routers
│  │  └─ notes_router.py      # /notes URL 처리
│  ├─ schemas
│  │  └─ note_schema.py       # 요청과 응답 데이터 모양
│  └─ services
│     └─ notes_service.py     # Supabase에 실제로 요청
├─ schema.sql                 # 테이블 생성 SQL
└─ tests                      # 앱을 실행하지 않고 확인하는 테스트
```

처음에는 `app/main.py` → `routers/notes_router.py` → `services/notes_service.py` 순서로 읽으면 됩니다.

## 1. Supabase 테이블 만들기

Supabase Dashboard의 **SQL Editor**에서 이 폴더의 [schema.sql](./schema.sql)을 실행합니다. `ex90_notes` 테이블이 만들어집니다.

## 2. 환경 변수 설정하기

`.env.example`을 복사해 같은 폴더에 `.env`를 만듭니다.

```powershell
Copy-Item .env.example .env
```

`.env`에는 실제 Supabase 값을 입력합니다.

```text
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

`SUPABASE_SERVICE_ROLE_KEY`는 서버에서만 사용하는 비밀 키입니다. GitHub, 화면, 문서에 실제 값을 넣지 마세요.

## 3. 서버 실행하기

```powershell
cd C:\aidevs\02_supabase-ai-backend\03_supabase-db-and-auth\90_structured-fastapi-examples\01_notes-api-with-supabase
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8011
```

브라우저에서 `http://127.0.0.1:8011/docs`를 열고 API를 실행합니다.

## 4. 사용 순서

먼저 `POST /notes`로 노트를 하나 만듭니다.

```json
{
  "title": "Supabase 첫 노트",
  "content": "router는 URL을 받고, service는 DB에 요청한다."
}
```

응답의 `id`를 복사한 뒤 아래 순서로 사용해 보세요.

1. `GET /notes` — 전체 목록 보기
2. `GET /notes/{note_id}` — 한 개 보기
3. `PUT /notes/{note_id}` — 제목과 내용 수정하기
4. `DELETE /notes/{note_id}` — 삭제하기

## 없는 노트는 어디서 처리하나요?

서비스는 DB에 데이터가 없으면 `None`(삭제는 `False`)만 반환합니다. 서비스는 HTTP를 알 필요가 없습니다.

```text
service: 노트 없음 → None 반환
router:  None 확인 → HTTP 404 응답
```

따라서 `GET`, `PUT`, `DELETE /notes/{note_id}`에서 없는 ID를 요청하면 라우터가 `404 Not Found`와 `{"detail": "Note not found"}`를 반환합니다.

Supabase 연결 정보가 없거나 DB 요청 자체가 실패한 경우는 데이터 없음과 다른 서버 문제입니다. 이 입문 예제에서는 오류를 숨기지 않고 FastAPI의 기본 500 오류로 확인합니다. 실제 서비스에서는 이후 공통 예외 핸들러와 로그를 추가해 별도로 다룹니다.

## 테스트

```powershell
python -m pytest tests
```

기본 테스트는 실제 Supabase DB를 호출하지 않습니다. 앱이 시작되고, `/health`와 Swagger의 노트 URL이 준비되었는지 확인합니다.
