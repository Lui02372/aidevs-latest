# Lab 100 - Project Structure Refactor

## 목표

`lab-99_mini-memo-api-server`에서 하나의 파일에 작성했던 메모 API를 실제 프로젝트에 가까운 폴더 구조로 분리합니다.

이 실습은 FastAPI의 기능을 새로 배우는 단계라기보다, 이미 만든 API를 역할별 파일로 나누는 리팩토링 실습입니다.

## 실습 전 기준

먼저 아래 실습을 끝낸 뒤 진행합니다.

```text
10_labs/lab-99_mini-memo-api-server
```

`lab-99`에서는 하나의 `solution.py` 안에 아래 내용이 모두 들어 있었습니다.

```text
FastAPI app 생성
Pydantic 요청/응답 모델
메모 저장소와 검색 로직
API endpoint
```

이번 실습에서는 위 내용을 아래처럼 나눕니다.

```text
app
├─ main.py
├─ routers
│  └─ memo_router.py
├─ schemas
│  └─ memo_schema.py
└─ services
   └─ memo_service.py

tests
└─ test_memo_api.py
```

## 역할 분리 기준

| 위치 | 역할 |
| --- | --- |
| `app/main.py` | FastAPI 앱 생성, router 등록 |
| `app/routers/memo_router.py` | API 경로, HTTP Method, 상태 코드 |
| `app/schemas/memo_schema.py` | Pydantic 요청/응답 모델 |
| `app/services/memo_service.py` | 메모 저장, 조회, 검색 같은 실제 처리 로직 |
| `tests/test_memo_api.py` | TestClient 기반 API 동작 확인 |

## 실행 방법

가상환경은 `02_supabase-ai-backend`의 `.venv`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
```

starter 실행:

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\starter
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

solution 실행:

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\solution
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

테스트 실행:

```powershell
pytest
```

`starter`의 테스트는 처음에는 실패하는 것이 정상입니다. TODO를 채우면서 실패 원인을 하나씩 해결하고, `solution` 폴더에서는 모든 테스트가 통과하는지 확인합니다.

## 요구사항

1. `app/main.py`에서는 `FastAPI()` 앱을 만들고 `memo_router`를 등록합니다.
2. `memo_schema.py`에는 `MemoCreate`, `MemoPublic`, `MemoListResponse` 모델을 둡니다.
3. `memo_service.py`에는 `list_memos`, `search_memos`, `get_memo`, `create_memo` 함수를 둡니다.
4. `memo_router.py`에는 `/health`, `/memos`, `/memos/search`, `/memos/{memo_id}`, `POST /memos` endpoint를 둡니다.
5. API 응답에는 `internal_note`가 포함되지 않아야 합니다.
6. `tests/test_memo_api.py`로 주요 API 동작을 확인합니다.

## 확인 질문

```text
1. main.py에 모든 코드를 두지 않고 router를 분리하면 어떤 점이 좋아지나요?
2. Pydantic 모델을 schemas 폴더에 두면 어떤 장점이 있나요?
3. service 함수는 API endpoint 함수와 무엇이 다른가요?
4. 이 구조를 Supabase 저장 로직으로 확장한다면 어느 파일이 가장 많이 바뀔까요?
```
