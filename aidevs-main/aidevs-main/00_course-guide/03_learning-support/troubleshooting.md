# Troubleshooting

오류가 나면 바로 코드를 고치기 전에 아래 순서로 확인합니다.

```text
1. 현재 폴더 위치가 맞는가?
2. .venv가 활성화되어 있는가?
3. 필요한 패키지를 설치했는가?
4. .env 파일 위치가 맞는가?
5. 실행 명령의 파일명과 app 이름이 맞는가?
6. 오류 메시지 첫 줄과 마지막 줄을 읽었는가?
```

## 막힘 지점별 빠른 링크

| 막히는 지점 | 먼저 확인할 곳 |
| --- | --- |
| Python 설치 문제 | [Python 설치 가이드](../02_setup-guides/01_python-install-guide.md), `python --version` |
| `.venv`, pip 문제 | [.venv, pip, requirements.txt](../02_setup-guides/06_venv-pip-requirements-guide.md), 각 과정 `SETUP.md` |
| PowerShell 실행 정책 오류 | [PowerShell과 터미널](../02_setup-guides/05_powershell-and-terminal-guide.md), `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| FastAPI 실행 오류 | 해당 과정 `SETUP.md`, `uvicorn` 실행 위치, `/docs` 접속 여부 |
| Streamlit에서 백엔드 연결 실패 | `API_BASE_URL`, 백엔드 `/docs`, `.env` 위치 |
| Supabase 프로젝트 생성, RLS, service role key 구분 | [Supabase 계정과 프로젝트](../02_setup-guides/09_supabase-account-guide.md), `02_supabase-ai-backend/SETUP.md` |
| Gemini/OpenAI API key, 비용, 호출 제한 | [Gemini/OpenAI 계정과 비용](../02_setup-guides/08_gemini-openai-account-guide.md), `02_llm-api-integration/02_api-key-and-billing` |
| LangGraph 상태 흐름 이해 | `05_llm-agent-orchestration/07_langgraph-workflow` |
| Docker Compose, 포트 충돌, `.env` 위치 | [Docker Desktop 설치 가이드](../02_setup-guides/14_docker-desktop-guide.md), `07_multi-agent-service-ops/SETUP.md` |
| AWS 계정과 비용 | [AWS 계정과 비용 관리](../02_setup-guides/15_aws-account-and-cost-guide.md), `07_multi-agent-service-ops/SETUP.md` |
| GitHub Actions 실패 | [GitHub Actions 가이드](../02_setup-guides/16_github-actions-guide.md), GitHub 저장소의 Actions 탭 |

## 질문할 때 포함할 내용

```text
실행 위치:
실행 명령:
오류 메시지:
관련 파일:
기대한 결과:
실제 결과:
이미 시도한 것:
```

실제 API Key나 token은 질문에 포함하지 않습니다.
