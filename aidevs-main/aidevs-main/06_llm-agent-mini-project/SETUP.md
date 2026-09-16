# SETUP

이 문서는 `06_llm-agent-mini-project`를 시작하기 위한 최소 환경 설정 안내입니다.

06 과정은 팀 프로젝트 과정입니다. 복잡한 운영 환경을 먼저 만들기보다, 로컬에서 LangGraph 기반 Agent 흐름을 실행하고 산출물을 완성하는 것을 우선합니다.

## 0. 공통 준비 문서

아래 항목이 아직 준비되지 않았다면 먼저 공통 설치 가이드를 확인합니다.

| 필요한 내용 | 문서 |
| --- | --- |
| Python과 `.venv` | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md), [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| OpenAI 계정, API Key, 비용 | [`../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md`](../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md) |
| Streamlit | [`../00_course-guide/02_setup-guides/11_streamlit-guide.md`](../00_course-guide/02_setup-guides/11_streamlit-guide.md) |
| 무료 배포 서비스 | [`../00_course-guide/02_setup-guides/13_free-deployment-services-guide.md`](../00_course-guide/02_setup-guides/13_free-deployment-services-guide.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |
| 문제 해결 | [`../00_course-guide/03_learning-support/troubleshooting.md`](../00_course-guide/03_learning-support/troubleshooting.md) |

## 1. 폴더 열기

VS Code에서 과정 폴더를 엽니다.

```powershell
cd C:\aidev\06_llm-agent-mini-project
code .
```

## 2. 가상환경 만들기

```powershell
cd C:\aidev\06_llm-agent-mini-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Python이 현재 과정의 `.venv`를 사용하는지 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
```

정상이라면 다음과 비슷한 경로가 나옵니다.

```text
C:\aidev\06_llm-agent-mini-project\.venv\Scripts\python.exe
```

## 3. 환경 변수 준비

```powershell
Copy-Item .env.example .env
```

`.env`에는 실제 API Key를 작성합니다. `.env`는 GitHub에 올리지 않습니다.

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

OpenAI API Key 없이도 Mock data 기반 Agent 구조 설계와 테스트 문서 작성은 진행할 수 있습니다.

## 4. 프로젝트 starter 복사

팀별 작업 폴더를 만들 때는 `02_project_structure`를 복사해서 시작할 수 있습니다.

```powershell
cd C:\aidev\06_llm-agent-mini-project
Copy-Item .\02_project_structure .\team-schedule-agent -Recurse
```

복사한 뒤에는 팀 프로젝트 폴더 안에서 구현을 진행합니다.

## 5. Backend 실행 흐름

starter의 backend는 FastAPI 기반 구조를 가정합니다.

```powershell
cd C:\aidev\06_llm-agent-mini-project\team-schedule-agent\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 확인합니다.

```text
http://127.0.0.1:8000/docs
```

## 6. Frontend 실행 흐름

```powershell
cd C:\aidev\06_llm-agent-mini-project\team-schedule-agent\frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Streamlit이 실행되면 브라우저에서 다음 주소를 확인합니다.

```text
http://localhost:8501
```

## 7. 선택 배포

06 과정에서는 배포를 필수로 보지 않습니다. 시간이 남을 때 다음 서비스를 참고합니다.

| 대상 | 무료 또는 저비용 선택지 |
| --- | --- |
| FastAPI backend | Render |
| Streamlit frontend | Streamlit Community Cloud |
| 환경 변수 | 각 배포 서비스의 Environment Variables 설정 |

Docker Compose, AWS, GitHub Actions, 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.

## 8. 시작 전 체크리스트

- [ ] `python -c "import sys; print(sys.executable)"` 결과가 06 과정 `.venv`를 가리킨다.
- [ ] `.env`를 만들었고 GitHub에 올리지 않는다.
- [ ] `02_project_structure`의 backend/frontend/docs 역할을 이해했다.
- [ ] 필수 산출물 2종을 확인했다.
- [ ] Mock data로 먼저 Agent 흐름을 구현한다.
