# AI Development Course

Python 기반 웹 API 개발에서 시작해 Supabase AI 서비스, Streamlit 인터페이스, LLM Agent, Docker 기반 운영, 멀티 에이전트 워크플로우까지 단계적으로 확장하는 AI 개발 과정입니다.

이 과정은 `01`부터 `08`까지 이어지며, 각 단계는 이전 단계에서 만든 개념과 구조를 다음 단계의 프로젝트로 확장합니다.

## 과정 구성

| 순서 | 과정 | 핵심 내용 | 문서 |
| --- | --- | --- | --- |
| 00 | Course Guide | 전체 과정 흐름, 설치 가이드, 공통 문제 해결 기준 | [README](./00_course-guide/README.md) |
| 01 | Python/Git Foundation | Python 기본 문법, 함수, 파일/JSON, 테스트, Git/GitHub, VS Code Source Control | [README](./01_python-git-foundation/README.md) / [SETUP](./01_python-git-foundation/SETUP.md) |
| 02 | Supabase AI Backend | FastAPI, Pydantic, Gemini API, Supabase DB/Auth/RLS, Upstash Redis, 백엔드 API | [README](./02_supabase-ai-backend/README.md) / [SETUP](./02_supabase-ai-backend/SETUP.md) |
| 03 | Supabase AI Frontend | Streamlit UI, API 호출, 로그인 상태, 챗봇 화면, 멀티페이지/탭 구조 | [README](./03_supabase-ai-frontend/README.md) / [SETUP](./03_supabase-ai-frontend/SETUP.md) |
| 04 | Supabase AI Mini Project | AI 서비스 로그 분석, Supabase 저장, Upstash Redis 이벤트 전달, SSE, 운영 대시보드 | [README](./04_supabase-ai-mini-project/README.md) / [SETUP](./04_supabase-ai-mini-project/SETUP.md) |
| 05 | LLM Agent Orchestration | Structured Output, LangChain, Tool Use, RAG, Memory, LangGraph, 승인·평가, FastAPI·Streamlit 연결 | [README](./05_llm-agent-orchestration/README.md) / [SETUP](./05_llm-agent-orchestration/SETUP.md) |
| 06 | LLM Agent Mini Project | 복합 API 연계 일정 조정 Agent, 자기 성찰, 피드백 루프, 결과 검증 | [README](./06_llm-agent-mini-project/README.md) / [SETUP](./06_llm-agent-mini-project/SETUP.md) |
| 07 | Multi-Agent Service Ops | 멀티 에이전트 협업, Docker Compose, GitHub Actions, AWS 배포, 모니터링, 보안 가드레일 | [README](./07_multi-agent-service-ops/README.md) / [SETUP](./07_multi-agent-service-ops/SETUP.md) |
| 08 | Multi-Agent Service Mini Project | Auto Healing 워크플로우, 장애 복구, 배포 검증, 파이프라인 결과 보고 | [README](./08_multi-agent-service-mini-project/README.md) / [SETUP](./08_multi-agent-service-mini-project/SETUP.md) |

## 진행 흐름

```text
01 Python/Git Foundation
-> 02 Supabase AI Backend
-> 03 Supabase AI Frontend
-> 04 Supabase AI Mini Project
-> 05 LLM Agent Orchestration
-> 06 LLM Agent Mini Project
-> 07 Multi-Agent Service Ops
-> 08 Multi-Agent Service Mini Project
```

각 단계의 역할은 다음과 같습니다.

| 단계 | 역할 |
| --- | --- |
| `01` | Python 실행, 테스트, Git/GitHub 흐름을 준비합니다. |
| `02` | FastAPI와 Supabase를 연결해 AI 백엔드 API를 만듭니다. |
| `03` | Streamlit으로 백엔드 API를 호출하는 프론트엔드 화면을 만듭니다. |
| `04` | 백엔드, DB, Redis 이벤트, SSE, 대시보드를 하나의 미니 프로젝트로 연결합니다. |
| `05` | Prompt, Tool, RAG, Memory, LangGraph 기반 단일 Agent 구조를 학습합니다. |
| `06` | 복합 API 연계 일정 조정 Agent 프로젝트를 구성합니다. |
| `07` | 멀티 에이전트 구조를 Docker, GitHub Actions, AWS 운영 환경으로 확장합니다. |
| `08` | Auto Healing 기반 멀티 에이전트 서비스 프로젝트로 마무리합니다. |

## 주요 기술

| 영역 | 기술 |
| --- | --- |
| Language | Python |
| Backend | FastAPI, Pydantic, Uvicorn |
| Frontend | Streamlit |
| Database/Auth | Supabase, PostgreSQL, Auth, RLS, JWT |
| LLM | Gemini API, OpenAI API |
| Cache/Event | Upstash Redis, Redis |
| Agent | LangChain, LangGraph, Tool Use, MCP, RAG, Memory |
| DevOps | Docker, Docker Compose, GitHub Actions, AWS ECR/App Runner, CloudWatch |
| AI Coding | Codex, ChatGPT, GitHub Copilot Chat |

## 설치와 환경 준비

공통 설치와 계정 준비는 [00_course-guide/02_setup-guides](./00_course-guide/02_setup-guides/README.md)에서 확인합니다.

| 필요한 내용 | 문서 |
| --- | --- |
| Python 설치 | [Python 설치 가이드](./00_course-guide/02_setup-guides/01_python-install-guide.md) |
| GitHub 계정과 VS Code 설치 | [VS Code 설치 가이드](./00_course-guide/02_setup-guides/02_vscode-install-guide.md) |
| VS Code 확장 프로그램 | [VS Code 확장 프로그램](./00_course-guide/02_setup-guides/03_vscode-extensions-guide.md) |
| Git/GitHub 설정 | [Git/GitHub 기본 설정](./00_course-guide/02_setup-guides/04_git-github-setup-guide.md) |
| PowerShell과 터미널 | [PowerShell과 터미널](./00_course-guide/02_setup-guides/05_powershell-and-terminal-guide.md) |
| `.venv`, `pip`, `requirements.txt` | [.venv, pip, requirements.txt](./00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| `.env`와 secret 보안 | [.env와 secret 보안](./00_course-guide/02_setup-guides/07_env-and-secret-guide.md) |
| Gemini/OpenAI 계정과 비용 | [Gemini/OpenAI 계정과 비용](./00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md) |
| Supabase | [Supabase 계정과 프로젝트](./00_course-guide/02_setup-guides/09_supabase-account-guide.md) |
| Upstash Redis | [Upstash Redis](./00_course-guide/02_setup-guides/10_upstash-redis-guide.md) |
| Streamlit | [Streamlit](./00_course-guide/02_setup-guides/11_streamlit-guide.md) |
| Postman | [Postman](./00_course-guide/02_setup-guides/12_postman-guide.md) |
| 무료 배포 서비스 | [무료 배포 서비스](./00_course-guide/02_setup-guides/13_free-deployment-services-guide.md) |
| Docker Desktop | [Docker Desktop](./00_course-guide/02_setup-guides/14_docker-desktop-guide.md) |
| AWS 계정과 비용 관리 | [AWS 계정과 비용 관리](./00_course-guide/02_setup-guides/15_aws-account-and-cost-guide.md) |
| GitHub Actions | [GitHub Actions](./00_course-guide/02_setup-guides/16_github-actions-guide.md) |
| Codex와 ChatGPT 사용 준비 | [Codex와 ChatGPT 사용 준비](./00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |

## 실행 기준

- `01`~`04`, `06`~`08`은 과정 최상위 `.venv` 하나를 기본으로 사용합니다.
- `05`는 단원별 의존성이 달라질 수 있어 단원별 `.venv` 방식을 우선 권장합니다.
- 각 과정의 실제 실행 명령은 해당 과정의 `SETUP.md`를 기준으로 합니다.
- `.env`, API Key, token, password는 GitHub에 올리지 않습니다.
- `.venv`, `__pycache__`, `.pytest_cache`, `site-packages`는 배포 또는 공유 대상에 포함하지 않습니다.

## 프로젝트 산출물

| 과정 | 프로젝트 주제 | 핵심 산출물 |
| --- | --- | --- |
| 04 | AI 서비스 로그 분석 및 운영 대시보드 구축 | API 설계서, 화면 설계서, DB 설계서, 대시보드 구현 결과물 |
| 06 | 복합 API 연계 일정 조정 Agent | 에이전트 아키텍처 설계서, 에이전트 시험 결과 보고서 |
| 08 | 에러 자가 치유(Auto Healing) 워크플로우 | 멀티 에이전트 아키텍처 설계서, 배포/장애 복구 보고서, 파이프라인 결과 보고서 |

## 문제 해결

공통 오류 해결 기준은 [문제 해결 가이드](./00_course-guide/03_learning-support/troubleshooting.md)에서 확인합니다.

자주 확인할 항목:

```text
현재 폴더 위치
.venv 활성화 여부
python -c "import sys; print(sys.executable)" 결과
requirements.txt 설치 여부
.env 파일 위치
API_BASE_URL 또는 서비스 URL
포트 충돌
Supabase, Upstash, Gemini/OpenAI key 설정
Docker Desktop 실행 여부
AWS 리소스와 비용 정리 여부
```

## 문서 구조

각 과정 폴더는 보통 다음 구조를 가집니다.

```text
README.md       과정 목표와 진행 순서
SETUP.md        설치, 환경 변수, 실행 방법
00_references   개념 설명과 참고 자료
10_labs         단계별 실습
20_assignments  과제
90_*            AI 보조 리뷰와 디버깅
99_*            최종 또는 통합 프로젝트
```
