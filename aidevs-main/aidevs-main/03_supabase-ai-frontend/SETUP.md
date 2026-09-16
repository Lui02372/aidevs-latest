# SETUP

`03_supabase-ai-frontend` 과정의 개발 환경 설정 문서입니다.

이 과정은 Streamlit 프론트엔드를 만들고, FastAPI 백엔드를 호출하는 방식으로 진행합니다. 처음에는 샘플 백엔드를 사용하고, 이후 `02_supabase-ai-backend` 또는 `99_final-frontend-project`의 `backend_mock`/`backend_service`와 연결합니다. React, SSE, Docker, AWS 운영 자동화는 필수가 아닙니다.

Streamlit 설치, 실행, widget, session state, form, layout, API 호출, secrets 관리의 전체 사용법은 [Streamlit 사용 가이드](./00_references/streamlit-usage-guide.md)를 참고합니다.

## 0. 공통 준비 문서

아래 항목이 아직 준비되지 않았다면 먼저 공통 설치 가이드를 확인합니다.

| 필요한 내용 | 문서 |
| --- | --- |
| Python 설치와 버전 확인 | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md) |
| VS Code 설치와 GitHub 로그인 | [`../00_course-guide/02_setup-guides/02_vscode-install-guide.md`](../00_course-guide/02_setup-guides/02_vscode-install-guide.md) |
| `.venv`, `pip`, `requirements.txt` | [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| `.env`와 secret 보안 | [`../00_course-guide/02_setup-guides/07_env-and-secret-guide.md`](../00_course-guide/02_setup-guides/07_env-and-secret-guide.md) |
| Streamlit 기본 사용법 | [`../00_course-guide/02_setup-guides/11_streamlit-guide.md`](../00_course-guide/02_setup-guides/11_streamlit-guide.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |
| 문제 해결 | [`../00_course-guide/03_learning-support/troubleshooting.md`](../00_course-guide/03_learning-support/troubleshooting.md) |

## 1. 작업 폴더로 이동

```powershell
cd C:\aidev\03_supabase-ai-frontend
Get-Location
```

결과가 아래와 비슷하면 됩니다.

```text
C:\aidev\03_supabase-ai-frontend
```

## 2. 가상환경 만들기

`03_supabase-ai-frontend` 폴더 안의 `.venv` 하나를 사용합니다.

```powershell
python -m venv .venv
```

특정 Python 3.12 실행 파일을 명확히 지정해야 한다면 아래처럼 실행할 수 있습니다.

```powershell
C:\Users\jeanm\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
```

이미 `.venv`가 있다면 다시 만들 필요가 없습니다.

## 3. 가상환경 활성화와 확인

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell 앞에 `(.venv)`가 보이면 활성화된 상태입니다.

VS Code에서 `C:\aidev` 루트를 열고 수업을 진행할 때는 현재 터미널이 어떤 Python을 사용하는지 먼저 확인합니다.

```powershell
echo $env:VIRTUAL_ENV
python -c "import sys; print(sys.executable)"
python --version
pip --version
```

정상이라면 아래처럼 `03_supabase-ai-frontend\.venv`를 가리킵니다.

```text
C:\aidev\03_supabase-ai-frontend\.venv
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\python.exe
```

## 4. 패키지 설치

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit --version
```

## 5. `.env` 파일 만들기

```powershell
Copy-Item .env.example .env
```

기본값은 로컬 백엔드 주소입니다.

```env
API_BASE_URL=http://127.0.0.1:8000
```

프론트엔드 `.env`에는 아래 값을 넣지 않습니다.

```text
SUPABASE_SERVICE_ROLE_KEY
GEMINI_API_KEY
OPENAI_API_KEY
UPSTASH_REDIS_REST_TOKEN
```

프론트엔드는 백엔드 주소만 알고, Supabase/Auth/LLM/Redis 처리는 백엔드가 담당합니다.

## 6. 첫 Streamlit 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

브라우저에서 아래 주소가 열리면 정상입니다.

```text
http://localhost:8501
```

## 7. API 연동 실습 전 백엔드 실행

`03_api-integration`부터는 백엔드가 먼저 실행되어 있어야 합니다. 백엔드는 수업 단계에 따라 다르게 선택합니다.

### 7-1. 샘플 백엔드

처음에는 프론트엔드 과정 안의 샘플 백엔드를 사용합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\03_api-integration\00_sample_backend
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### 7-2. 05 챗봇 샘플 백엔드

`05_ai-chatbot-interface`에서 챗봇 UI와 백엔드 chat API를 연결할 때는 챗봇 전용 샘플 백엔드를 사용합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

mock 응답만 사용할 때는 `.env`가 없어도 됩니다.

Gemini 실제 호출 API(`/api/chat/gemini`)를 사용할 때만 이 백엔드 폴더 안에 백엔드 전용 `.env`를 만듭니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend
Copy-Item .env.example .env
```

백엔드 전용 `.env` 예시:

```env
GEMINI_API_KEY=실제-Gemini-API-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

주의할 점:

```text
C:\aidev\03_supabase-ai-frontend\.env
-> Streamlit 프론트엔드용
-> API_BASE_URL만 둡니다.

C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend\.env
-> 챗봇 FastAPI 백엔드용
-> GEMINI_API_KEY를 둡니다.
```

프론트엔드 화면 코드는 `GEMINI_API_KEY`를 읽지 않습니다. Streamlit은 백엔드 API 주소만 알고, Gemini 호출은 FastAPI 백엔드가 처리합니다.

### 7-3. 02 과정 백엔드

실제 Supabase 저장과 인증 흐름은 `02_supabase-ai-backend`의 FastAPI 서버를 실행해 연결합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 7-4. 99 최종 프로젝트 backend_mock

최종 프론트엔드 프로젝트의 필수 실습은 `backend_mock`으로 진행합니다. Supabase, Gemini, Redis 없이 바로 실행됩니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### 7-5. 99 최종 프로젝트 backend_service

실제 Supabase Auth, Supabase DB, Gemini, 선택형 Upstash Redis, Render 배포까지 확인할 때만 `backend_service`를 사용합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`backend_service`를 사용하기 전에는 `backend_service\.env.example`을 참고해 `backend_service\.env`를 만들고, Supabase SQL Editor에서 `schema.sql`을 실행합니다.

## 8. 학습 순서

1. `01_streamlit-basic`: 화면 실행, 입력, 기본 레이아웃
2. `02_streamlit-ui-components`: 버튼, 폼, 표, 차트
3. `03_api-integration`: FastAPI 호출, 로딩/오류 처리
4. `04_state-session-and-data`: session state, token, Authorization header, 대화 이력
5. `05_ai-chatbot-interface`: mock 기반 챗봇 UI와 챗봇 전용 백엔드 호출
6. `06_streamlit-multipage-app`: `st.Page`, `st.navigation()` 기반 왼쪽 메뉴 구조, 화면 분리, 팀 개발 방식
7. `07_streamlit-tabs-app`: `st.tabs()` 기반 탭 구조, 탭별 파일 분리 방식
8. `90_ai-assisted-ui-review-and-debugging`: 오류 분석과 UI 리뷰
9. `99_final-frontend-project`: `backend_mock` 기반 개인화 AI 챗봇 통합 UX 구현, 선택형 `backend_service` 배포 연결

## 9. 오류 확인 순서

1. 현재 위치가 `C:\aidev\03_supabase-ai-frontend`인지 확인합니다.
2. `python -c "import sys; print(sys.executable)"` 결과가 현재 과정 `.venv`인지 확인합니다.
3. `pip install -r requirements.txt`를 실행했는지 확인합니다.
4. 백엔드 서버가 `http://127.0.0.1:8000/docs`에서 열리는지 확인합니다.
5. `.env`의 `API_BASE_URL`이 백엔드 주소와 같은지 확인합니다.
6. 8000 포트가 이미 사용 중이면 기존 백엔드를 종료하거나 다른 포트로 실행합니다.
7. Streamlit 화면에서 오류가 나면 터미널의 파일명과 줄 번호를 확인합니다.

## 10. 이 과정에서 다루지 않는 것

```text
Supabase DB 직접 접속
service role key를 프론트엔드에 저장
LLM API key를 프론트엔드에 저장
SSE 본격 구현
Docker Compose
AWS 배포
GitHub Actions 운영 자동화
```

SSE 기반 실시간 응답 스트리밍은 `04_supabase-ai-mini-project`에서 통합 실습으로 다룹니다. Docker/AWS/GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.
