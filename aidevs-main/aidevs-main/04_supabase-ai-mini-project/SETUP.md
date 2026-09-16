# SETUP

이 문서는 `04_supabase-ai-mini-project` 개발 환경 설정 문서입니다.

04 과정은 과정 최상위 `.venv` 하나를 사용합니다. 하위 `backend`, `frontend` 폴더 안에 별도 `.venv`를 만들지 않습니다.

## 0. 공통 준비 문서

아래 항목이 아직 준비되지 않았다면 먼저 공통 설치 가이드를 확인합니다.

| 필요한 내용 | 문서 |
| --- | --- |
| Python과 `.venv` | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md), [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| Supabase 계정과 프로젝트 | [`../00_course-guide/02_setup-guides/09_supabase-account-guide.md`](../00_course-guide/02_setup-guides/09_supabase-account-guide.md) |
| Upstash Redis | [`../00_course-guide/02_setup-guides/10_upstash-redis-guide.md`](../00_course-guide/02_setup-guides/10_upstash-redis-guide.md) |
| Streamlit | [`../00_course-guide/02_setup-guides/11_streamlit-guide.md`](../00_course-guide/02_setup-guides/11_streamlit-guide.md) |
| Render, Streamlit Cloud, Supabase Cloud, Upstash 배포 | [`../00_course-guide/02_setup-guides/13_free-deployment-services-guide.md`](../00_course-guide/02_setup-guides/13_free-deployment-services-guide.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |
| 문제 해결 | [`../00_course-guide/03_learning-support/troubleshooting.md`](../00_course-guide/03_learning-support/troubleshooting.md) |

## 1. 작업 폴더로 이동

```powershell
cd C:\aidev\04_supabase-ai-mini-project
Get-Location
```

## 2. 가상환경 만들기

```powershell
python -m venv .venv
```

## 3. 가상환경 활성화 확인

```powershell
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python --version
pip --version
```

정상이라면 Python 경로가 다음처럼 보입니다.

```text
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\python.exe
```

## 4. 패키지 설치

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5. `.env` 파일 만들기

```powershell
Copy-Item .env.example .env
```

필수 환경 변수:

```env
API_BASE_URL=http://127.0.0.1:8000
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
REDIS_URL=
```

`REDIS_URL`은 Upstash Redis의 `rediss://...` URL을 입력합니다. 이번 과정에서는 로컬 Redis를 설치하지 않습니다. Upstash Redis URL이 아직 준비되지 않았다면 임시로 비워 둘 수 있고, 이때 예제는 메모리 fallback으로 동작합니다. 다만 04 과정의 기본 개념은 **DB는 영구 저장소, Upstash Redis는 실시간 이벤트 전달, SSE는 화면 표시 통로**라는 역할 구분입니다.

정리하면 다음과 같습니다.

```text
기본 실습/최종 설계 기준: Upstash Redis 포함
수업 실행 안정성: Upstash URL이 아직 없으면 임시 memory fallback으로 SSE 흐름 확인
```

## 6. Supabase 테이블 만들기

작은 실행 예제는 다음 SQL을 사용합니다.

```text
C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\schema.sql
```

최종 프로젝트 starter는 다음 SQL을 사용합니다.

```text
C:\aidev\04_supabase-ai-mini-project\03_project_structure\database\schema.sql
```

Supabase SQL Editor에서 필요한 SQL을 실행한 뒤 Table Editor에서 테이블이 생성되었는지 확인합니다.

## 7. 01 실습 실행

PowerShell 1: backend 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

PowerShell 2: frontend 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\frontend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 8. 최종 프로젝트 starter 실행

`03_project_structure`는 학생용 최종 프로젝트 starter입니다. 기본 코드는 `/health`와 backend 연결 확인, 그리고 두 가지 Streamlit frontend 구조를 제공합니다. 로그 API, SSE, 피드백 API, 대시보드 화면은 학생들이 직접 구현합니다.

backend:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

frontend는 두 방식 중 하나를 선택해서 실행합니다.

왼쪽 메뉴 방식:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_multipage
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

탭 방식:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_tabs
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 9. 오류 확인 순서

1. 현재 Python이 `04_supabase-ai-mini-project\.venv`를 가리키는지 확인합니다.
2. `python -m pip install -r requirements.txt`를 실행했는지 확인합니다.
3. backend가 `http://127.0.0.1:8000/docs`에서 열리는지 확인합니다.
4. Streamlit의 `API_BASE_URL`과 backend 주소가 같은지 확인합니다.
5. Supabase 환경 변수와 테이블 생성 여부를 확인합니다.
6. Upstash Redis URL이 아직 없어도 임시 memory fallback으로 기본 SSE가 보이는지 확인합니다.
7. 8000 또는 8501 포트가 이미 사용 중이면 기존 프로세스를 종료합니다.

## 10. backend 테스트

01 실습 backend:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m pytest tests -q
```

03 starter backend:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m pytest tests -q
```

## 11. 자주 나는 오류

### Supabase 테이블을 찾을 수 없음

다음과 비슷한 오류가 나오면 Supabase SQL Editor에서 `schema.sql`을 아직 실행하지 않았거나, `.env`가 다른 Supabase 프로젝트를 가리키고 있는 상태입니다.

```text
Could not find the table 'public.realtime_service_logs'
Could not find the table 'public.ai_answer_feedback'
```

확인 순서:

1. `.env`의 `SUPABASE_URL`이 현재 Supabase 프로젝트와 같은지 확인합니다.
2. Supabase SQL Editor에서 필요한 `schema.sql` 전체를 실행합니다.
3. Table Editor에서 테이블이 생성되었는지 확인합니다.
4. FastAPI backend를 재시작합니다.

### 실행 파일이 차단됨

`uvicorn.exe` 또는 `pytest.exe`가 애플리케이션 제어 정책에 의해 차단되면 직접 실행하지 말고 아래처럼 실행합니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m pytest tests -q
```
