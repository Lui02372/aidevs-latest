# 06_service-log-and-integration-check

서비스 로그 조회 화면과 프론트엔드 통합 점검 방법을 학습합니다.

이 단원은 로그를 프론트엔드에서 직접 저장하는 수업이 아닙니다. 실제 서비스 로그 저장은 `02_supabase-ai-backend`와 Supabase가 담당합니다. Streamlit은 백엔드 API를 호출해 최근 로그를 조회하고, 현재 UI-백엔드-데이터 연결 상태를 눈으로 확인할 수 있게 보여줍니다.

## 학습 목표

- 백엔드 서비스 로그 API를 호출할 수 있다.
- Authorization header가 필요한 로그 조회 API를 호출할 수 있다.
- 로그 목록을 표와 요약 지표로 표시할 수 있다.
- 백엔드 미실행, token 누락, API 주소 오류를 화면에서 구분해 안내할 수 있다.
- 실제 배포 전에 확인해야 할 항목을 체크리스트로 정리할 수 있다.

## 예제 파일

```text
01_service-log-dashboard.py
02_integration-readiness-check.py
03_free-deployment-guide.md
```

## 백엔드 연결 기준

실제 수업에서는 `02_supabase-ai-backend`의 서비스 로그 API와 연결합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
C:\aidev\02_supabase-ai-backend\99_final-backend-project
```

백엔드 서버 실행 예시는 다음과 같습니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

백엔드가 아직 준비되지 않았을 때는 프론트엔드 폴더의 샘플 백엔드를 사용할 수 있습니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 프론트엔드 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\06_service-log-and-integration-check\01_service-log-dashboard.py
```

## 확인 내용

- `API_BASE_URL`이 현재 백엔드 주소와 맞는가?
- 로그인 token 또는 수업용 token이 요청 header에 포함되는가?
- 서비스 로그가 표로 표시되는가?
- 오류가 발생했을 때 이해할 수 있는 안내 메시지가 보이는가?
- 실제 배포 전에 확인할 항목을 설명할 수 있는가?

## 최종 배포 안내

이 단원에서는 초보자가 따라 할 수 있는 무료 배포 서비스 기반의 최종 배포 흐름을 안내합니다.

```text
FastAPI 백엔드 -> Render
Redis 캐시/세션 -> Upstash
Streamlit 프론트엔드 -> Streamlit Community Cloud
```

자세한 단계는 다음 문서를 확인합니다.

```text
03_free-deployment-guide.md
```

Docker, Docker Compose, AWS, GitHub Actions를 사용하는 운영 자동화와 모니터링은 `07_multi-agent-service-ops`에서 더 깊게 다룹니다.
