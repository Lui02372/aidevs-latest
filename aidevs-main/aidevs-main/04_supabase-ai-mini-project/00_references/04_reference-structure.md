# 04 Reference Structure

04 미니 프로젝트의 backend/frontend 구조는 `03_supabase-ai-frontend/99_final-frontend-project`를 참고합니다.

참고 위치:

```text
C:\aidev\03_supabase-ai-frontend\99_final-frontend-project
```

## 참고할 내용

| 참고 대상 | 04에서 적용할 내용 |
| --- | --- |
| `backend_mock` | 프론트엔드가 막히지 않게 동작하는 작은 backend 예제 흐름 |
| `backend_service` | `app/main.py`, `core`, `routers`, `schemas`, `services` 구조 |
| `solution/app.py` | `API_BASE_URL`로 backend를 호출하는 Streamlit 구조 |
| `templates` | 화면 설계, API 흐름, 배포 점검 문서 작성 방식 |
| `checklist` | 완성 후 스스로 점검하는 문서 형식 |

## 04 최종 프로젝트 권장 구조

```text
project
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  ├─ core
│  │  ├─ routers
│  │  ├─ schemas
│  │  └─ services
│  ├─ tests
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend
│  ├─ app.py
│  └─ requirements.txt
├─ database
│  └─ schema.sql
└─ docs
   ├─ api-design.md
   ├─ screen-design.md
   ├─ database-design.md
   ├─ dashboard-result-report.md
   └─ deployment-note.md
```

## 중요한 기준

- 프론트엔드는 Supabase에 직접 접속하지 않습니다.
- 프론트엔드는 Redis에 직접 접속하지 않습니다.
- 프론트엔드는 `API_BASE_URL`로 FastAPI만 호출합니다.
- Supabase service role key와 Redis URL은 backend에만 둡니다.
- DB SQL은 `database/schema.sql`에 둡니다.
- 산출물은 `docs`에 작성하되, `02_project-deliverables`의 샘플 기준을 참고합니다.
