# 10_labs

이 폴더는 `01_fastapi-backend` 단원에서 수업 중 함께 진행하는 실습 모음입니다.

앞의 `01_fastapi-project-setup`부터 `04_async-and-external-api`까지 배운 내용을 메모 API 흐름으로 반복 연습합니다. 대부분의 lab은 `starter.py`를 먼저 열어 TODO를 채우고, 막히면 `solution.py`와 비교합니다.

마지막 `lab-100_project-structure-refactor`는 실제 프로젝트 구조를 익히기 위해 `starter/app`, `solution/app`, `tests` 폴더를 사용합니다.

## 실습 목록

| 순서 | 폴더 | 연결 단원 | 핵심 내용 |
| --- | --- | --- | --- |
| 1 | `lab-01_fastapi-health-check` | `01_fastapi-project-setup` | FastAPI 앱 생성, `/`, `/health` |
| 2 | `lab-02_memo-routing-and-search` | `02_routing-and-request` | Path Parameter, Query Parameter, 메모 검색 |
| 3 | `lab-03_memo-request-validation` | `03_pydantic-and-response` | Pydantic 요청 검증, 422 오류 |
| 4 | `lab-04_memo-response-model` | `03_pydantic-and-response` | Response Model, 내부 값 제외 |
| 5 | `lab-05_async-external-context` | `04_async-and-external-api` | async/await, 외부 API 데이터 연결 |
| 6 | `lab-06_memo-crud-review` | `02~04 복습` | 메모 CRUD 전체 흐름 복습 |
| 99 | `lab-99_mini-memo-api-server` | `01_fastapi-backend 마무리` | 작은 메모 API 서버 완성 |
| 100 | `lab-100_project-structure-refactor` | `01_fastapi-project-setup` 구조 확장 | `app/main.py`, `routers`, `schemas`, `services`, `tests` 분리 |

## 공통 실행 방법

가상환경은 `02_supabase-ai-backend` 폴더의 `.venv`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

각 lab 폴더로 이동한 뒤 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-01_fastapi-health-check
uvicorn starter:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn starter:app --reload
```

정답 파일을 실행할 때는 다음처럼 실행합니다.

```powershell
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

`lab-100_project-structure-refactor`는 폴더 구조가 다르므로 아래처럼 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-100_project-structure-refactor\solution
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

테스트는 같은 위치에서 실행합니다.

```powershell
python -m pytest
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

서버 종료:

```text
Ctrl + C
```

## 진행 방법

```text
1. README.md에서 목표와 요구사항을 확인합니다.
2. starter.py의 TODO를 하나씩 채웁니다.
3. uvicorn starter:app --reload로 실행합니다.
4. Swagger UI에서 API를 직접 호출합니다.
5. 동작이 다르면 solution.py와 비교합니다.
6. 왜 다르게 동작했는지 코드 주석과 함께 확인합니다.
```

## 확인 기준

```text
FastAPI 기본:
  앱이 실행되고 /health가 {"status": "ok"}를 반환합니다.

라우팅:
  Path Parameter와 Query Parameter를 구분해 사용할 수 있습니다.

요청 검증:
  잘못된 요청을 보냈을 때 422 오류가 발생합니다.

응답 모델:
  내부 관리 값이 API 응답에 노출되지 않습니다.

비동기 처리:
  await와 외부 API 호출 구조를 설명할 수 있습니다.

마무리 실습:
  작은 메모 API 서버를 스스로 완성하고, 프로젝트 폴더 구조로 분리할 수 있습니다.
```
