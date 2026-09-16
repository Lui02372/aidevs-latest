# Backend Starter

이 폴더는 최종 프로젝트의 FastAPI backend starter입니다. 기본 코드는 `/health`만 제공합니다.

## 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## 기본 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 상태 확인 |

## 학생 구현 API

| Method | URL | 구현 위치 |
| --- | --- | --- |
| POST | `/logs` | `app/routers/log_router.py` |
| GET | `/logs` | `app/routers/log_router.py` |
| GET | `/logs/summary` | `app/routers/log_router.py` |
| GET | `/stream/logs` | `app/routers/log_router.py` 또는 `stream_router.py` |
| POST | `/feedback` | `app/routers/feedback_router.py` |
| GET | `/feedback` | `app/routers/feedback_router.py` |

구현 예시는 `01_realtime-log-dashboard-practice/backend/app`을 참고합니다.

## 테스트

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m pytest tests -q
```
