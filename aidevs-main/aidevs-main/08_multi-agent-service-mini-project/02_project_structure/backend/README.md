# backend

FastAPI 기반 Auto Healing API 서버를 구현하는 폴더입니다.

## 담당 기능

- `/health`: 서비스 상태 확인
- `/incidents`: 장애 이벤트 접수
- `/recoveries/{incident_id}`: 복구 결과 조회

## 실행 예시

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure\backend
uvicorn app.main:app --reload
```

Docker Compose로 실행할 때는 상위 `02_project_structure` 폴더에서 실행합니다.
